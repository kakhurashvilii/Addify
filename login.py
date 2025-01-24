import json
import os
from telethon import TelegramClient
import sys

CONFIG_FILE = "config.json"
SESSION_FOLDER = "sessions"

# Helper function to load configuration
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {}

# Helper function to save configuration
def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


# Helper function to add new accounts to config
async def add_accounts_to_config(config):
    while True:
        try:
            print("\n🆕 ახალი ანგარიშის დამატება")
            account_name = input("შეიყვანეთ ანგარიშის სახელი (მაგ. user1): ")
            api_id = int(input("შეიყვანეთ API ID: "))
            api_hash = input("შეიყვანეთ API HASH: ")

            session_name = input("შეიყვანეთ სესიის სახელი (მაგ. session_user1): ")
            if not session_name:
                session_name = f"session_{account_name}" if account_name else "session_default"

            # Ensure that the session folder exists
            if not os.path.exists(SESSION_FOLDER):
                os.makedirs(SESSION_FOLDER)

            session_path = os.path.join(SESSION_FOLDER, session_name)
            phone_number = input("შეიყვანეთ თქვენი მობილურის ნომერი (მაგ. +995595000000): ")

            # Add the new account to the configuration
            config[account_name] = {
                "api_id": api_id,
                "api_hash": api_hash,
                "session_name": session_path,
                "phone_number": phone_number
            }

            # Save configuration after adding the new account
            save_config(config)
            print(f"✅ ახალი ანგარიში დამატებულია: {account_name} ({session_path})")

            # Attempt login process after adding new account
            client = TelegramClient(
                session_path,
                api_id,
                api_hash,
            )

            print(f"📡 Telegram API-სთან კავშირის მცდელობა... ({account_name})")
            await client.connect()

            # If phone number exists, proceed with verification process
            if phone_number:
                if not await client.is_user_authorized():
                    print(f"⚠️ {account_name} - ვერ მოხერხდა ავტორიზაცია. გადაგზავნილია კოდი.")
                    await client.send_code_request(phone_number)
                    code = input(f"შეიყვანეთ კოდი, რომელიც გამოგიგზავნათ {phone_number}: ")
                    await client.sign_in(phone_number, code)
                    print(f"✅ {account_name} ანგარიშით ავტორიზაცია წარმატებით მოხდა!")
                else:
                    print(f"✅ {account_name} უკვე ავტორიზებულია.")
        except EOFError:
            print("Input error: The system was unable to receive input.")
            account_name = "default_account"  # Fallback value
        except Exception as e:
            print(f"Error: {e}")
            account_name = "default_account"  # Fallback value

        add_another = input("გსურთ კიდევ ერთი ანგარიშის დამატება? (y/n): ")
        if add_another.lower() != 'y':  # Check if the user doesn't want to add another account
            break  # Exit the loop if 'n' is entered

# Helper function to edit existing account information
def edit_account_config(config):
    print("\n✏️ ანგარიშის რედაქტირება")
    account_name = input("შეიყვანეთ ანგარიშის სახელი, რომელსაც გსურთ რედაქტირება (მაგ. user1): ")

    if account_name not in config:
        print(f"⚠️ {account_name} - ანგარიშის სახელი არ არსებობს!")
        return

    print(f"\n📝 {account_name} ანგარიშის რედაქტირება")
    api_id = input(f"შეიყვანეთ ახალი API ID (მეორე შეცვლის შემთხვევაში ჩაასხვავეთ): ")
    if api_id:
        config[account_name]["api_id"] = int(api_id)

    api_hash = input(f"შეიყვანეთ ახალი API HASH (მეორე შეცვლის შემთხვევაში ჩაას Differეთ): ")
    if api_hash:
        config[account_name]["api_hash"] = api_hash

    session_name = input(f"შეიყვანეთ ახალი სესიის სახელი (მეორე შეცვლის შემთხვევაში ჩაას Differეთ): ")
    if session_name:
        config[account_name]["session_name"] = os.path.join(SESSION_FOLDER, session_name)

    phone_number = input(f"შეიყვანეთ ახალი მობილურის ნომერი (მაგ. +995595000000): ")
    if phone_number:
        config[account_name]["phone_number"] = phone_number

    save_config(config)
    print(f"✅ {account_name} ანგარიში წარმატებით შეიცვალა!")

# Login function using the above helpers
# Existing login function
async def login():
    clients = {}

    accounts = load_config()

    for account_name, account_data in accounts.items():
        session_name = account_data["session_name"]
        api_id = account_data["api_id"]
        api_hash = account_data["api_hash"]
        phone_number = account_data["phone_number"]

        client = TelegramClient(session_name, api_id, api_hash)
        await client.connect()

        # Check if the client is authorized
        if not await client.is_user_authorized():
            print(f"⚠️ {session_name} - ვერ მოხერხდა ავტორიზაცია. გადაგზავნილია კოდი.")
            await client.send_code_request(phone_number)
            code = input(f"შეიყვანეთ კოდი, რომელიც გამოგიგზავნათ {phone_number}: ")
            await client.sign_in(phone_number, code)

        # Store the client in the dictionary under the session name
        clients[session_name] = client
        print(f"✅ {session_name} ავტორიზაცია წარმატებით მოხდა!")

    return clients


# Function to check if the user is authorized
async def is_authorized(client: TelegramClient):
    return await client.is_user_authorized()

