import csv
import asyncio
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest

async def add_members(client):
    target_group = input("შეიყვანეთ სამიზნე ჯგუფის @username: ")
    try:
        group = await client.get_entity(target_group)

        with open("members.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # სათაურის გამოტოვება
            for row in reader:
                user_id, username, name = row
                try:
                    user = await client.get_input_entity(username)
                    await client(InviteToChannelRequest(group, [user]))
                    print(f"✅ დამატებულია: {username}")
                    await asyncio.sleep(random.randint(60, 120))  # პაუზა flood-limit-ის თავიდან ასაცილებლად
                except PeerFloodError:
                    print("⚠️ Flood Error! გაჩერდით 10 წუთით.")
                    await asyncio.sleep(600)
                except UserPrivacyRestrictedError:
                    print(f"❌ {username} - მომხმარებელს აქვს პრივატულობის შეზღუდვა.")
                except Exception as e:
                    print(f"❌ ვერ დაემატა {username}: {e}")
    except Exception as e:
        print(f"❌ შეცდომა ჯგუფზე წვდომისას: {e}")
