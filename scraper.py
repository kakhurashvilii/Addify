from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

async def scrape_members(client):
    group_username = input("შეიყვანეთ ჯგუფის @username: ")
    limit = int(input("რამდენი წევრი უნდა ამოიღოთ? "))
    
    try:
        # ჯგუფის ინფორმაციის მიღება
        group = await client.get_entity(group_username)
        
        # წევრების მიღება
        participants = []
        offset = 0
        while True:
            chunk = await client(GetParticipantsRequest(
                channel=group,
                filter=ChannelParticipantsSearch(''),
                offset=offset,
                limit=limit,
                hash=0
            ))
            if not chunk.users:
                break
            participants.extend(chunk.users)
            offset += len(chunk.users)
            if len(participants) >= limit:
                break

        # მონაცემების ფაილში შენახვა
        with open("members.csv", "w", encoding="utf-8") as file:
            file.write("ID,Username,Name\n")
            for user in participants[:limit]:  # თუ მეტი წევრი აიღო, დავზღუდოთ
                user_id = user.id
                username = user.username or "None"
                name = f"{user.first_name or ''} {user.last_name or ''}".strip()
                file.write(f"{user_id},{username},{name}\n")
        
        print(f"✅ {len(participants)} წევრი დამწერილია members.csv-ში")
    except Exception as e:
        print(f"❌ შეცდომა: {e}")

