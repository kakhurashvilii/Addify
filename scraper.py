import csv
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

# 1. ყველა წევრის სკრიპტი
async def scrape_all_members(client, group_username):
    try:
        group = await client.get_entity(group_username)
        members = await client.get_participants(group)
        with open("all_members.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username", "Name"])
            for member in members:
                writer.writerow([member.id, member.username, member.first_name])
        print("✅ ყველა წევრი შეინახა all_members.csv-ში!")
    except Exception as e:
        print(f"❌ შეცდომა: {e}")

# 2. ონლაინ წევრების სკრიპტი
async def scrape_online_members(client, group_username):
    try:
        group = await client.get_entity(group_username)
        members = await client.get_participants(group, online_only=True)
        with open("online_members.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username", "Name"])
            for member in members:
                writer.writerow([member.id, member.username, member.first_name])
        print("✅ ონლაინ წევრები შეინახა online_members.csv-ში!")
    except Exception as e:
        print(f"❌ შეცდომა: {e}")

# 3. აქტიური წევრების სკრიპტი
async def scrape_active_members(client, group_username, days=7):
    try:
        group = await client.get_entity(group_username)
        members = await client.get_participants(group)
        with open("active_members.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username", "Name"])
            for member in members:
                if member.status and member.status.was_online and \
                   (datetime.now() - member.status.was_online).days <= days:
                    writer.writerow([member.id, member.username, member.first_name])
        print("✅ აქტიური წევრები შეინახა active_members.csv-ში!")
    except Exception as e:
        print(f"❌ შეცდომა: {e}")

# 4. კვირეული წევრების სკრიპტი
async def scrape_weekly_members(client, group_username):
    await scrape_active_members(client, group_username, days=7)

# 5. თვიური წევრების სკრიპტი
async def scrape_monthly_members(client, group_username):
    await scrape_active_members(client, group_username, days=30)

# 6. Hidden წევრების სკრიპტი
async def scrape_hidden_members(client, group_username):
    print("⚠️ Hidden წევრების სკრაპინგი ჯერ არ არის გაწერილი.")

# 7. Premium წევრების სკრიპტი
async def scrape_premium_members(client, group_username):
    print("⚠️ Premium წევრების სკრაპინგი ჯერ არ არის გაწერილი.")

# 8. არაექტიური წევრების სკრიპტი
async def scrape_non_active_members(client, group_username, days=30):
    try:
        group = await client.get_entity(group_username)
        members = await client.get_participants(group)
        with open("non_active_members.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username", "Name"])
            for member in members:
                if member.status and member.status.was_online and \
                   (datetime.now() - member.status.was_online).days > days:
                    writer.writerow([member.id, member.username, member.first_name])
        print("✅ არაექტიური წევრები შეინახა non_active_members.csv-ში!")
    except Exception as e:
        print(f"❌ შეცდომა: {e}")
