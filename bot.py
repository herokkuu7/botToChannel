import os
import asyncio
import logging
from aiohttp import web
from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait, RPCError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Environment Variables
BOT_TOKEN = os.environ.get(BOT_TOKEN)
API_ID = int(os.environ.get(API_ID))
API_HASH = os.environ.get(API_HASH)
# Render provides a PORT env var. Default to 8080 if not found.
PORT = int(os.environ.get(PORT, 8080))

# State management
user_data = {}

app = Client(my_bot, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- Dummy Web Server for Render ---
async def web_server()
    async def handle(request)
        return web.Response(text=Bot is running!)

    app = web.Application()
    app.router.add_get(, handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 0.0.0.0, PORT)
    await site.start()
    logger.info(fWeb server started on port {PORT})

# --- Bot Commands ---

@app.on_message(filters.command(start))
async def start_command(client, message)
    await message.reply_text(
        👋 Bot Storage Batchernn
        1. Send `set -100xxxx` to set destination.n
        2. Find the filemessage in this chat you want to start with.n
        3. Reply to that message with `batchFromBotTOChannel`.n
        4. Enter the number of messages to clone.
    )

@app.on_message(filters.command(set))
async def set_destination(client, message)
    if len(message.command)  2
        await message.reply_text(❌ Usage `set -100123456789`)
        return
    
    dest = message.command[1]
    try
        chat = await client.get_chat(dest)
        user_data[message.from_user.id] = {dest_id chat.id}
        await message.reply_text(f✅ Destination set to {chat.title})
    except Exception as e
        await message.reply_text(f❌ Error Make sure I am Admin in that channel.nLog {e})

@app.on_message(filters.command(batchFromBotTOChannel) & filters.reply)
async def set_start_point(client, message)
    uid = message.from_user.id
    if uid not in user_data or dest_id not in user_data[uid]
        await message.reply_text(❌ Please set a destination channel first using `set`.)
        return

    start_id = message.reply_to_message.id
    user_data[uid][start_msg_id] = start_id
    user_data[uid][step] = waiting_for_count
    
    await message.reply_text(
        f📍 Start Point Set (ID {start_id})nn
        How many messages do you want to clone downwards (Send a number)
    )

@app.on_message(filters.command(batchFromBotTOChannel) & ~filters.reply)
async def warn_no_reply(client, message)
    await message.reply_text(⚠️ You must Reply to the message you want to start copying from with `batchFromBotTOChannel`.)

@app.on_message(filters.text & filters.create(lambda _, __, m m.text.isdigit()))
async def process_batch(client, message)
    uid = message.from_user.id
    if uid in user_data and user_data[uid].get(step) == waiting_for_count
        target_count = int(message.text)
        dest_id = user_data[uid][dest_id]
        start_id = user_data[uid][start_msg_id]
        source_chat_id = message.chat.id 
        
        status_msg = await message.reply_text(f🚀 Processing {target_count} messages...)
        
        copied_count = 0
        current_id = start_id
        safety_break = 0 
        MAX_SEARCH = target_count + 500

        while copied_count  target_count and safety_break  MAX_SEARCH
            try
                if current_id == message.id 
                    current_id += 1
                    continue

                await client.copy_message(chat_id=dest_id, from_chat_id=source_chat_id, message_id=current_id)
                copied_count += 1
                await asyncio.sleep(1.5)
            
            except FloodWait as e
                await asyncio.sleep(e.value + 1)
                continue
            except RPCError
                pass
            except Exception as e
                logger.error(fError on {current_id} {e})
            
            current_id += 1
            safety_break += 1
            
            if copied_count % 10 == 0 and copied_count  0
                await status_msg.edit_text(f⏳ Progress {copied_count}{target_count})

        user_data[uid][step] = None
        await status_msg.edit_text(f✅ Done!nCloned {copied_count} messages to channel.)

# --- Main Async Loop ---
async def main()
    await app.start()
    print(Bot Started...)
    
    # Start the web server
    await web_server()
    
    # Keep the bot running
    await idle()
    
    await app.stop()

if __name__ == __main__
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())