import os
import csv
import asyncio
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from login import login  # იმპორტირებული ავტორიზაციის ფუნქცია

# Windows-ზე asyncio-ს სწორად მუშაობისთვის
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# მომხმარებლების წაკითხვა CSV-დან
def read_users_from_csv(csv_filename):
    users = []
    with open(csv_filename, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header row if present
        for row in reader:
            if len(row) >= 2 and row[1].strip():  # Check if username is present
                users.append({
                    'id': row[0].strip(),
                    'username': row[1].strip(),
                    'name': row[2].strip() if len(row) > 2 else ""
                })
            else:
                print(f"⚠️ Skipping invalid row: {id}")
    return users


# FloodWaitError-ის დალაგება
async def handle_floodwait(client, error_seconds, wait_threshold, rest_time):
    if error_seconds > wait_threshold:
        print(f"⚠️ FloodWaitError: ლოდინის დრო {error_seconds} წამია, რაც აღემატება ზღვარს ({wait_threshold}). გადართვა სხვა ანგარიშზე.")
        return False  # გადართვა სხვა ანგარიშზე
    else:
        print(f"🕒 FloodWaitError: ლოდინი {error_seconds} წამი.")
        await asyncio.sleep(error_seconds)
        return True  # გაგრძელება იმავე ანგარიშით

# წევრების დამატების ფუნქცია
async def add_members(client, group, user):
    try:
        if not user['username']:
            print(f"⚠️ Skipping user without username: ID {user['id']}")
            return False

        # Resolving the user entity
        entity = await client.get_entity(user['username'])

        # Check if the user is already in the group
        participants = await client.get_participants(group)
        if any(p.id == entity.id for p in participants):
            print(f"⚠️ {user['username']} already in the group. Skipping.")
            return False

        # Add user to group
        await client(InviteToChannelRequest(group, [entity]))
        print(f"✅ Successfully added: {user['username']}")
        return True

    except ValueError:
        print(f"⚠️ Cannot resolve entity: {user['username']}. Skipping.")
        return False
    except FloodWaitError as e:
        print(f"⚠️ Flood wait error: {e.seconds} seconds. Pausing...")
        await asyncio.sleep(e.seconds)
        return False
    except Exception as e:
        print(f"❌ Failed to add {user['username']}: {e}")
        return False


# main loop for adding all members
# main loop for adding all members

# Save the last processed index to a file
def save_last_processed_index(index, filename="last_processed_index.txt"):
    with open(filename, "w") as file:
        file.write(str(index))
        print(f"✅ Saved last processed index: {index}")

# Read the last processed index from a file
def read_last_processed_index(filename="last_processed_index.txt"):
    if not os.path.exists(filename):
        print(f"📄 File {filename} does not exist. Starting from 0.")
        return 0  # Default to start from the beginning
    with open(filename, "r") as file:
        content = file.read().strip()
        if content.isdigit():  # Check if the content is a valid integer
            print(f"📖 Read last processed index: {content}")
            return int(content)
        else:
            print(f"⚠️ Invalid content in {filename}. Resetting to 0.")
            return 0

# Main loop for adding all members
async def add_all_members(clients):
    if not clients:
        print("⚠️ No authorized accounts found. Exiting.")
        return

    target_group = input("Enter the target group @username: ")
    MAX_MEMBERS = int(input("Enter the maximum number of members per account (default: 50): ") or 50)
    ADD_INTERVAL = int(input("Enter the interval between adding members in seconds (default: 10): ") or 10)
    MAX_WAIT_TIME = int(input("Enter flood error wait time in seconds (default: 100): ") or 100)
    REST_INTERVAL = int(input("Enter rest interval in seconds (default: 86400): ") or 86400)

    # Reading CSV file for users
    csv_filename = "members/all_members.csv"
    users = read_users_from_csv(csv_filename)

    if not users:
        print(f"⚠️ No users found in CSV file: {csv_filename}")
        return

    last_added_user_index = read_last_processed_index()  # Read from the saved index

    for account_name, client in clients.items():
        print(f"🔄 Starting to add members with account: {account_name}")
        added_count = 0  # Reset added count for each session

        # Try to find the group
        try:
            group = await client.get_entity(target_group)  # Get group entity
            if group:
                print(f"✅ Group found: {target_group}")
        except Exception as e:
            print(f"❌ Group search failed for {target_group}: {e}")
            continue

        # Iterate over each user and try adding them
        for index, user in enumerate(users[last_added_user_index:], start=last_added_user_index):
            if added_count >= MAX_MEMBERS:
                print(f"📡 Maximum members added ({MAX_MEMBERS}). Switching to the next account.")
                save_last_processed_index(index)  # Save last index for the next session
                last_added_user_index = index
                break

            try:
                success = await add_members(client, group, user)
                if success:
                    added_count += 1
                    print(f"✅ Added: {user['username']} ({added_count}/{len(users)})")
                    save_last_processed_index(index + 1)  # Save progress after each successful addition
                    last_added_user_index = index + 1
                    await asyncio.sleep(ADD_INTERVAL or 10)  # Wait between additions
            except FloodWaitError as e:
                print(f"⏳ FloodWaitError: Waiting for {e.seconds} seconds.")
                if e.seconds > MAX_WAIT_TIME:
                    print(f"⚠️ Waiting time exceeds the threshold ({MAX_WAIT_TIME} seconds). Switching to next account.")
                    save_last_processed_index(index)  # Save last index for the next session
                    last_added_user_index = index
                    break  # Switch to the next account
                else:
                    print(f"🕒 Waiting for {e.seconds} seconds.")
                    await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"❌ Unexpected error with {user['username']}: {str(e).splitlines()[0]}")

        # After finishing with one account, switch to another
        if added_count < len(users):
            print(f"📆 Resting for {REST_INTERVAL} seconds before switching to next account.")
            await asyncio.sleep(REST_INTERVAL or 100)  # Rest time before switching accounts

    print("🎉 All accounts and users processed!")


async def add_online_members(client):
    target_group = input("შეიყვანეთ სამიზნე ჯგუფის @username: ")
    group = await client.get_entity(target_group)
    members = await read_csv_file("members/online_members.csv")

    added_count = 0
    for row in members:
        if added_count >= MAX_MEMBERS:
            break

        user_id, username, name = row
        if await add_member(client, group, username):
            added_count += 1

# 3. აქტიური წევრების დამატება
async def add_active_members(client):
    target_group = input("შეიყვანეთ სამიზნე ჯგუფის @username: ")
    group = await client.get_entity(target_group)
    members = await read_csv_file("members/active_members.csv")

    added_count = 0
    for row in members:
        if added_count >= MAX_MEMBERS:
            break

        user_id, username, name = row
        if await add_member(client, group, username):
            added_count += 1

# 4. არაექტიური წევრების დამატება
async def add_non_active_members(client):
    target_group = input("შეიყვანეთ სამიზნე ჯგუფის @username: ")
    group = await client.get_entity(target_group)
    members = await read_csv_file("members/non_active_members.csv")

    added_count = 0
    for row in members:
        if added_count >= MAX_MEMBERS:
            break

        user_id, username, name = row
        if await add_member(client, group, username):
            added_count += 1

# საერთო ფუნქცია წევრის დამატებისთვის


# asyncio.run(add_all_members(client))  # ვუწოდებთ შესაბამის ფუნქციას საჭირო ადგილას
