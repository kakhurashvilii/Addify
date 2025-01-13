from telethon import TelegramClient
from config import API_ID, API_HASH, SESSION_NAME
from scraper import scrape_members
from adder import add_members
from messenger import send_message

# Telegram Client-ის ინიციალიზაცია
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def main():
    print("📡 Telegram API-სთან კავშირის მცდელობა...")
    await client.start()
    
    while True:
        print("\n🔧 მენიუ:")
        print("1. წევრების სკრაპინგი")
        print("2. წევრების დამატება")
        print("3. შეტყობინების გაგზავნა")
        print("4. გამოსვლა")
        
        choice = input("აირჩიეთ (1-4): ")
        
        if choice == "1":
            await scrape_members(client)
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
