async def send_message(client):
    target = input("შეიყვანეთ ჯგუფის/მომხმარებლის @username: ")
    message = input("შეიყვანეთ გასაგზავნი შეტყობინება: ")
    try:
        await client.send_message(target, message)
        print(f"✅ შეტყობინება გაიგზავნა {target}-ზე")
    except Exception as e:
        print(f"❌ შეცდომა: {e}")
