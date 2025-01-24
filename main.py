import asyncio
from login import add_accounts_to_config, edit_account_config, is_authorized, load_config, login, save_config
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
from adder import (
    add_all_members,
    add_online_members,
    add_active_members,
    add_non_active_members
)
from messenger import send_message
import aioconsole  # type: ignore # To handle non-blocking input

async def show_active_users():
    config = load_config()
    active_users = []

    for account, details in config.items():
        if is_authorized(details):
            active_users.append(account)

    print(f"\n🔑 აქტიური მომხმარებლები:")
    if active_users:
        for user in active_users:
            print(f"✅ {user}")
    else:
        print("❌ არ არის აქტიური მომხმარებლები.")

async def user_menu(clients):
    while True:
        print("\n👤 მომხმარებლის მენიუ:")
        print("1. ახალი მომხმარებლის დამატება")
        print("2. მონიტორინგი/რედაქტირება (მონაცემების შეცვლა)")
        print("3. სკრაპინგი/დამატება/შეტყობინებები")
        print("4. აქტიური მომხმარებლები")
        print("5. გამოსვლა")

        choice = await aioconsole.ainput("აირჩიეთ (1-5): ")

        if choice == "1":
            config = load_config()
            await add_accounts_to_config(config)

        elif choice == "2":
            print("\n🛠️ მონაცემების რედაქტირება:")
            print("1.1. API ID რედაქტირება")
            print("1.2. API HASH რედაქტირება")
            print("1.3. მობილურის ნომრის რედაქტირება")
            print("1.4. უკან დაბრუნება")
            
            sub_choice = await aioconsole.ainput("აირჩიეთ (1.1-1.4): ")
            if sub_choice == "1.1":
                account_name = await aioconsole.ainput("შეიყვანეთ ანგარიშის სახელი, რომლის API ID-საც შეცვლით: ")
                new_api_id = int(await aioconsole.ainput("შეიყვანეთ ახალი API ID: "))
                config = load_config()
                if account_name in config:
                    config[account_name]["api_id"] = new_api_id
                    save_config(config)
                    print(f"✅ API ID წარმატებით შეიცვალა {account_name}-ში.")
                else:
                    print("❌ ასეთი ანგარიში არ არსებობს!")
            elif sub_choice == "1.2":
                account_name = await aioconsole.ainput("შეიყვანეთ ანგარიშის სახელი, რომლის API HASH-საც შეცვლით: ")
                new_api_hash = await aioconsole.ainput("შეიყვანეთ ახალი API HASH: ")
                config = load_config()
                if account_name in config:
                    config[account_name]["api_hash"] = new_api_hash
                    save_config(config)
                    print(f"✅ API HASH წარმატებით შეიცვალა {account_name}-ში.")
                else:
                    print("❌ ასეთი ანგარიში არ არსებობს!")
            elif sub_choice == "1.3":
                account_name = await aioconsole.ainput("შეიყვანეთ ანგარიშის სახელი, რომლის მობილურის ნომრის შეცვლას გსურთ: ")
                new_phone_number = await aioconsole.ainput("შეიყვანეთ ახალი მობილურის ნომერი (მაგ. +995595000000): ")
                config = load_config()
                if account_name in config:
                    config[account_name]["phone_number"] = new_phone_number
                    save_config(config)
                    print(f"✅ მობილურის ნომერი წარმატებით შეიცვალა {account_name}-ში.")
                else:
                    print("❌ ასეთი ანგარიში არ არსებობს!")
            elif sub_choice == "1.4":
                continue
            else:
                print("❌ არასწორი არჩევანი!")

        elif choice == "3":
            print("\n🔧 მენიუ:")
            print("1. წევრების სკრაპინგი (კატეგორია)")
            print("2. წევრების დამატება (კატეგორია)")
            print("3. შეტყობინების გაგზავნა")
            print("4. დაბრუნება")

            sub_choice = await aioconsole.ainput("აირჩიეთ (1-4): ")

            if sub_choice == "1":
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
                
                sub_sub_choice = await aioconsole.ainput("აირჩიეთ (1.1-1.9): ")
                if sub_sub_choice == "1.1":
                    group_username = await aioconsole.ainput("შეიყვანეთ ჯგუფის @username: ")
                    await scrape_all_members(clients, group_username)
                elif sub_sub_choice == "1.2":
                    group_username = await aioconsole.ainput("შეიყვანეთ ჯგუფის @username: ")
                    await scrape_online_members(clients, group_username)
                elif sub_sub_choice == "1.3":
                    group_username = await aioconsole.ainput("შეიყვანეთ ჯგუფის @username: ")
                    await scrape_active_members(clients, group_username)
                elif sub_sub_choice == "1.4":
                    group_username = await aioconsole.ainput("შეიყვანეთ ჯგუფის @username: ")
                    await scrape_weekly_members(clients, group_username)
                elif sub_sub_choice == "1.5":
                    group_username = await aioconsole.ainput("შეიყვანეთ ჯგუფის @username: ")
                    await scrape_monthly_members(clients, group_username)
                elif sub_sub_choice == "1.6":
                    group_username = await aioconsole.ainput("შეიყვანეთ ჯგუფის @username: ")
                    await scrape_hidden_members(clients, group_username)
                elif sub_sub_choice == "1.7":
                    group_username = await aioconsole.ainput("შეიყვანეთ ჯგუფის @username: ")
                    await scrape_premium_members(clients, group_username)
                elif sub_sub_choice == "1.8":
                    group_username = await aioconsole.ainput("შეიყვანეთ ჯგუფის @username: ")
                    await scrape_non_active_members(clients, group_username)
                elif sub_sub_choice == "1.9":
                    continue
                else:
                    print("❌ არასწორი არჩევანი!")

            elif sub_choice == "2":
                print("\n📂 დამატების კატეგორია:")
                print("  2.1. ყველა წევრის დამატება")
                print("  2.2. ონლაინ წევრების დამატება ჯგუფში")
                print("  2.3. აქტიური წევრების დამატება ჯგუფში")
                print("  2.4. არაექტიური წევრების დამატება ჯგუფში")
                print("  2.5. უკან დაბრუნება")

                sub_sub_choice = await aioconsole.ainput("აირჩიეთ (2.1-2.5): ")
                if sub_sub_choice == "2.1":
                    await add_all_members(clients)
                elif sub_sub_choice == "2.2":
                    await add_online_members(clients)
                elif sub_sub_choice == "2.3":
                    await add_active_members(clients)
                elif sub_sub_choice == "2.4":
                    await add_non_active_members(clients)
                elif sub_sub_choice == "2.5":
                    continue
                else:
                    print("❌ არასწორი არჩევანი!")

            elif sub_choice == "3":
                await send_message(clients)

            elif sub_choice == "4":
                continue

        elif choice == "4":
            await show_active_users()

        elif choice == "5":
            print("🚪 გამოსვლა...")
            break

        else:
            print("❌ არასწორი არჩევანი!")

async def main():
    clients = await login()

    await user_menu(clients)

if __name__ == "__main__":
    asyncio.run(main())
