import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Environment Variables থেকে ডেটা নেওয়া হচ্ছে
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
SOURCE_CHANNEL = int(os.environ.get("SOURCE_CHANNEL"))

app = Client(
    "file_store_bot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    if len(message.command) > 1:
        file_id = message.command[1]
        try:
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=SOURCE_CHANNEL,
                message_id=int(file_id)
            )
        except Exception:
            await message.reply("❌ ফাইলটি খুঁজে পাওয়া যায়নি।")
    else:
        await message.reply("👋 ফাইল পাঠান, আমি লিংক তৈরি করে দেব।")

@app.on_message(filters.document | filters.video | filters.photo | filters.audio)
async def store_file(client, message):
    try:
        sent_msg = await message.copy(chat_id=SOURCE_CHANNEL)
        bot_username = (await client.get_me()).username
        share_link = f"https://t.me/{bot_username}?start={sent_msg.id}"
        
        await message.reply(
            f"✅ **লিংক তৈরি হয়েছে:**\n`{share_link}`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 ফাইলটি দেখুন", url=share_link)]
            ])
        )
    except Exception as e:
        await message.reply(f"❌ এরর: {str(e)}")

app.run()
