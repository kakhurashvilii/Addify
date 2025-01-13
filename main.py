from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME
from scraper import (
    scrape_all_members,
    scrape_online_members,
    scrape_active_members,
    scrape_weekly_members,
    scrape_monthly_members,
    scrape_hidden_members,
    scrape_premium_members,
    scrape_non_active_members
)
from adder import add_members
from messenger import send_message

# Telegram Client-ის ინიციალიზაცია
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def main():
    print("📡 Telegram API-სთან კავშირის მცდელობა...")
    await client.start()

    while True:
        print("\n🔧 მენიუ:")
        print("1. წევრების სკრაპინგი (კატეგორია)")
        print("2. წევრების დამატება")
        print("3. შეტყობინების გაგზავნა")
        print("4. გამოსვლა")

        choice = input("აირჩიეთ (1-4): ")

        if choice == "1":
            print("\n📂 სკრაპინგის კატეგორია:")
            print("  1.1. ყველა წევრის სკრაპინგი")
            print("  1.2. ონლაინ წევრების სკრაპინგი")
            print("  1.3. აქტიური წევრების სკრაპინგი")
            print("  1.4. კვირეული წევრების სკრაპინგი")
            print("  1.5. თვიური წევრების სკრაპინგი")
            print("  1.6. Hidden წევრების სკრაპინგი")
            print("  1.7. Premium წევრების სკრაპინგი")
            print("  1.8. არაექტიური წევრების სკრაპინგი")
            print("  1.9. უკან დაბრუნება")
            
            sub_choice = input("აირჩიეთ (1.1-1.9): ")
            if sub_choice == "1.1":
                group_username = input("შეიყვანეთ ჯგუფის @username: ")
                await scrape_all_members(client, group_username)
            elif sub_choice == "1.2":
                group_username = input("შეიყვანეთ ჯგუფის @username: ")
                await scrape_online_members(client, group_username)
            elif sub_choice == "1.3":
                group_username = input("შეიყვანეთ ჯგუფის @username: ")
                await scrape_active_members(client, group_username)
            elif sub_choice == "1.4":
                group_username = input("შეიყვანეთ ჯგუფის @username: ")
                await scrape_weekly_members(client, group_username)
            elif sub_choice == "1.5":
                group_username = input("შეიყვანეთ ჯგუფის @username: ")
                await scrape_monthly_members(client, group_username)
            elif sub_choice == "1.6":
                group_username = input("შეიყვანეთ ჯგუფის @username: ")
                await scrape_hidden_members(client, group_username)
            elif sub_choice == "1.7":
                group_username = input("შეიყვანეთ ჯგუფის @username: ")
                await scrape_premium_members(client, group_username)
            elif sub_choice == "1.8":
                group_username = input("შეიყვანეთ ჯგუფის @username: ")
                await scrape_non_active_members(client, group_username)
            elif sub_choice == "1.9":
                continue
            else:
                print("❌ არასწორი არჩევანი!")
        elif choice == "2":
            await add_members(client)
        elif choice == "3":
            await send_message(client)
        elif choice == "4":
            print("🚪 გამოსვლა...")
            break
        else:
            print("❌ არასწორი არჩევანი!")

with client:
    client.loop.run_until_complete(main())
