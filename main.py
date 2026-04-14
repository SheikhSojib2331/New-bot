import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# আপনার দেওয়া তথ্যগুলো এখানে সেট করা হয়েছে
API_ID = 24475059
API_HASH = "941c93397999ed7c1e9198a757535af8"
BOT_TOKEN = "8009049442:AAHsEpWKXHThS4fGBDC4LlfQRBxHt01P8SI"
SOURCE_CHANNEL = -1003736867646

app = Client("file_store_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    if len(message.command) > 1:
        file_id = message.command[1]
        try:
            # সোর্স চ্যানেল থেকে ফাইলটি কপি করে ইউজারের কাছে পাঠাবে
            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=SOURCE_CHANNEL,
                message_id=int(file_id)
            )
        except Exception as e:
            await message.reply("❌ দুঃখিত, ফাইলটি খুঁজে পাওয়া যায়নি বা ডিলিট করা হয়েছে।")
    else:
        await message.reply(
            "👋 **হ্যালো! আমি একটি অ্যাডভান্সড ফাইল স্টোর বট।**\n\n"
            "যেকোনো ফাইল আমাকে পাঠান, আমি সেটিকে চ্যানেলে সেভ করে আপনাকে একটি শেয়ারিং লিংক দেব।"
        )

@app.on_message(filters.document | filters.video | filters.photo | filters.audio)
async def store_file(client, message):
    processing_msg = await message.reply("📤 ফাইলটি সেভ করা হচ্ছে, দয়া করে অপেক্ষা করুন...")
    
    try:
        # ফাইলটি সোর্স চ্যানেলে ফরওয়ার্ড করা হচ্ছে
        sent_msg = await message.copy(chat_id=SOURCE_CHANNEL)
        
        # ইউনিক শেয়ারিং লিংক তৈরি
        bot_username = (await client.get_me()).username
        share_link = f"https://t.me/{bot_username}?start={sent_msg.id}"
        
        await processing_msg.edit_text(
            f"✅ **ফাইলটি সফলভাবে সেভ করা হয়েছে!**\n\n"
            f"🔗 **আপনার ফাইল লিংক:**\n`{share_link}`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔗 ফাইলটি দেখুন", url=share_link)]
            ])
        )
    except Exception as e:
        await processing_msg.edit_text(f"❌ এরর: {str(e)}\n\nনিশ্চিত করুন যে বটটি আপনার সোর্স চ্যানেলে অ্যাডমিন হিসেবে আছে।")

print("বটটি সফলভাবে চালু হয়েছে!")
app.run()
