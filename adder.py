from telethon.tl.functions.contacts import AddContactRequest

async def add_members(client):
    target_group = input("შეიყვანეთ სამიზნე ჯგუფის @username: ")
    
    try:
        with open("members.csv", "r", encoding="utf-8") as file:
            lines = file.readlines()[1:]  # გამოტოვეთ პირველი სტრიქონი
            for line in lines:
                user_id, username, name = line.strip().split(",")
                try:
                    await client(AddContactRequest(int(user_id), username, name, ""))
                    print(f"✅ დამატებულია: {username}")
                except Exception as e:
                    print(f"❌ ვერ დაემატა {username}: {e}")
    except Exception as e:
        print(f"❌ შეცდომა ფაილში: {e}")
