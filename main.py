import os
from pyrogram import Client, filters
import asyncio

# কনফিগারেশন (Environment Variables থেকে তথ্য নেবে)
API_ID = int(os.environ.get("API_ID", 24475059))
API_HASH = os.environ.get("API_HASH", "941c93397999ed7c1e9198a757535af8")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8009049442:AAHsEpWKXHThS4fGBDC4LlfQRBxHt01P8SI")
SOURCE_CHANNEL = int(os.environ.get("SOURCE_CHANNEL", -1003736867646))

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def send_latest(client, message):
    try:
        # চ্যানেল থেকে সর্বশেষ ১টি মেসেজ খুঁজে বের করা
        async for last_message in client.get_chat_history(SOURCE_CHANNEL, limit=1):
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=SOURCE_CHANNEL,
                message_id=last_message.id
            )
    except Exception as e:
        await message.reply_text(f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")

print("বটটি সক্রিয় হয়েছে...")
app.run()
