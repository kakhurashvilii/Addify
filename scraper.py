import csv
from datetime import datetime
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import UserStatusOnline, UserStatusOffline, UserStatusRecently
from telethon.tl.types import InputPeerEmpty
from login import is_authorized
import os
# 1. ყველა წევრის სკრიპტი
# ფუნქცია, რომელიც ამოწმებს, არის თუ არა კლიენტი ავტორიზებული
async def is_authorized(client):
    try:
        await client.get_me()
        return True
    except:
        return False

# ყველა წევრის დამუშავების ფუნქცია
async def scrape_all_members(clients, group_username):
    print("⏳ გთხოვთ, აირჩიოთ ანგარიშის სახელწოდება:")
    for index, account_name in enumerate(clients.keys(), 1):
        print(f"{index}. {account_name}")
    
    # მომხმარებლის არჩევის მენიუ
    choice = int(input(f"აირჩიეთ (1-{len(clients)}): "))
    selected_account_name = list(clients.keys())[choice - 1]
    client = clients[selected_account_name]

    if not await is_authorized(client):
        print(f"⚠️ {selected_account_name} - ვერ მოხერხდა ავტორიზაცია!")
        return

    try:
        group = await client.get_entity(group_username)
        members = await client.get_participants(group)

        # დირექტორიის შექმნა
        if not os.path.exists("members"):
            os.makedirs("members")

        with open("members/all_members.csv", "w", encoding="utf-8", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['sr. no.', 'username', 'user id', 'access hash', 'name', 'group', 'group id', 'last seen', 'message_author'])
            
            for idx, member in enumerate(members, start=1):
                # Access hash
                access_hash = getattr(member, "access_hash", None)

                # Last seen
                if isinstance(member.status, UserStatusRecently):
                    last_seen = "Recently"
                elif isinstance(member.status, UserStatusOnline):
                    last_seen = "Online"
                elif isinstance(member.status, UserStatusOffline):
                    last_seen = f"Offline ({member.status.was_online})"
                else:
                    last_seen = "Unknown"

                # Message author (placeholder, requires additional logic)
                message_author = None  # თუ საჭიროა, დაამატეთ შესაბამისი ლოგიკა

                # Member's full name
                name = f"{member.first_name or ''} {member.last_name or ''}".strip()

                # Writing data to CSV
                writer.writerow([
                    idx, 
                    member.username or "N/A", 
                    member.id, 
                    access_hash, 
                    name, 
                    group.title, 
                    group.id, 
                    last_seen, 
                    message_author
                ])

        print(f"✅ ყველა წევრი შეინახა members/all_members.csv-ში!")
    except Exception as e:
        print(f"❌ შეცდომა: {e} - {selected_account_name}")

# 2. ონლაინ წევრების სკრიპტი
async def scrape_online_members(clients, group_username):
    print("⏳ გთხოვთ, აირჩიოთ ანგარიშის სახელწოდება:")
    for index, account_name in enumerate(clients.keys(), 1):
        print(f"{index}. {account_name}")
    
    # მომხმარებლის არჩევის მენიუ
    choice = int(input(f"აირჩიეთ (1-{len(clients)}): "))
    selected_account_name = list(clients.keys())[choice - 1]
    client = clients[selected_account_name]

    if not await is_authorized(client):
        print(f"⚠️ {selected_account_name} - ვერ მოხერხდა ავტორიზაცია!")
        return

    try:
        group = await client.get_entity(group_username)
        members = await client.get_participants(group)
        
        # მხოლოდ ონლაინ წევრების ფილტრაცია
        online_members = [
            member for member in members 
            if isinstance(member.status, (UserStatusOnline, UserStatusRecently))
        ]
        
        with open(f"members/online_members.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username", "Name"])
            for member in online_members:
                # თუ წევრს აქვს username, otherwise წერენ "" (ცარიელი)
                username = member.username if member.username else "N/A"
                writer.writerow([member.id, username, member.first_name])

        print(f"✅ ონლაინ წევრები შეინახა online_members.csv-ში!")
    except Exception as e:
        print(f"❌ შეცდომა: {e} - {selected_account_name}")

# 3. აქტიური წევრების სკრიპტი
async def scrape_active_members(clients, group_username, days=7):
    print("⏳ გთხოვთ, აირჩიოთ ანგარიშის სახელწოდება:")
    for index, account_name in enumerate(clients.keys(), 1):
        print(f"{index}. {account_name}")
    
    # მომხმარებლის არჩევის მენიუ
    choice = int(input(f"აირჩიეთ (1-{len(clients)}): "))
    selected_account_name = list(clients.keys())[choice - 1]
    client = clients[selected_account_name]

    if not await is_authorized(client):
        print(f"⚠️ {selected_account_name} - ვერ მოხერხდა ავტორიზაცია!")
        return

    try:
        group = await client.get_entity(group_username)
        members = await client.get_participants(group)
        with open(f"members/active_members.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username", "Name"])
            for member in members:
                if member.status and member.status.was_online and \
                   (datetime.now() - member.status.was_online).days <= days:
                    writer.writerow([member.id, member.username, member.first_name])
        print(f"✅ აქტიური წევრები შეინახა active_members.csv-ში!")
    except Exception as e:
        print(f"❌ შეცდომა: {e} - {selected_account_name}")

# 4. კვირეული წევრების სკრიპტი
async def scrape_weekly_members(clients, group_username):
    await scrape_active_members(clients, group_username, days=7)

# 5. თვიური წევრების სკრიპტი
async def scrape_monthly_members(clients, group_username):
    await scrape_active_members(clients, group_username, days=30)

# 6. Hidden წევრების სკრიპტი
async def scrape_hidden_members(clients, group_username):
    print("⚠️ Hidden წევრების სკრაპინგი ჯერ არ არის გაწერილი.")
    print("⏳ გთხოვთ, აირჩიოთ ანგარიშის სახელწოდება:")
    for index, account_name in enumerate(clients.keys(), 1):
        print(f"{index}. {account_name}")
    
    # მომხმარებლის არჩევის მენიუ
    choice = int(input(f"აირჩიეთ (1-{len(clients)}): "))
    selected_account_name = list(clients.keys())[choice - 1]
    client = clients[selected_account_name]

    if not await is_authorized(client):
        print(f"⚠️ {selected_account_name} - ვერ მოხერხდა ავტორიზაცია!")
        return

    try:
        group = await client.get_entity(group_username)
        participants = await client.get_participants(group)
        
        # ვივარაუდოთ, რომ hidden წევრებს აქვთ შეზღუდული სტატუსი
        hidden_members = [participant for participant in participants if participant.restricted]
        
        with open(f"members/hidden_members.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username", "Name"])  # თავიდან დავწეროთ თავები
            for member in hidden_members:
                writer.writerow([member.id, member.username, member.first_name])
        
        print(f"✅ Hidden წევრები შეინახა hidden_members.csv-ში!")
    except Exception as e:
        print(f"❌ შეცდომა: {e} - {selected_account_name}")

# 7. Premium წევრების სკრაპინგი
async def scrape_premium_members(clients, group_username):
    print("⚠️ Premium წევრების სკრაპინგი ჯერ არ არის გაწერილი.")
    print("⏳ გთხოვთ, აირჩიოთ ანგარიშის სახელწოდება:")
    for index, account_name in enumerate(clients.keys(), 1):
        print(f"{index}. {account_name}")
    
    # მომხმარებლის არჩევის მენიუ
    choice = int(input(f"აირჩიეთ (1-{len(clients)}): "))
    selected_account_name = list(clients.keys())[choice - 1]
    client = clients[selected_account_name]

    if not await is_authorized(client):
        print(f"⚠️ {selected_account_name} - ვერ მოხერხდა ავტორიზაცია!")
        return

    try:
        group = await client.get_entity(group_username)
        participants = await client.get_participants(group)
        
        # ვივისუფაროთ, რომ premium წევრებს აქვთ 'premium' ატრიბუტი
        premium_members = [participant for participant in participants if hasattr(participant, 'premium') and participant.premium]
        
        with open(f"members/premium_members.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username", "Name"])  # თავიდან დავწეროთ თავები
            for member in premium_members:
                writer.writerow([member.id, member.username, member.first_name])
        
        print(f"✅ Premium წევრები შეინახა premium_members.csv-ში!")
    except Exception as e:
        print(f"❌ შეცდომა: {e} - {selected_account_name}")

# 8. არაექტიური წევრების სკრიპტი
async def scrape_non_active_members(clients, group_username, days=30):
    print("⏳ გთხოვთ, აირჩიოთ ანგარიშის სახელწოდება:")
    for index, account_name in enumerate(clients.keys(), 1):
        print(f"{index}. {account_name}")
    
    # მომხმარებლის არჩევის მენიუ
    choice = int(input(f"აირჩიეთ (1-{len(clients)}): "))
    selected_account_name = list(clients.keys())[choice - 1]
    client = clients[selected_account_name]

    if not await is_authorized(client):
        print(f"⚠️ {selected_account_name} - ვერ მოხერხდა ავტორიზაცია!")
        return

    try:
        group = await client.get_entity(group_username)
        members = await client.get_participants(group)
        with open(f"members/non_active_members.csv", "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username", "Name"])
            for member in members:
                if member.status and member.status.was_online and \
                   (datetime.now() - member.status.was_online).days > days:
                    writer.writerow([member.id, member.username, member.first_name])
        print(f"✅ არაექტიური წევრები შეინახა non_active_members.csv-ში!")
    except Exception as e:
        print(f"❌ შეცდომა: {e} - {selected_account_name}")
