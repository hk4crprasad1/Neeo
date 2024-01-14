import os
import asyncio
import aiosqlite
from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    Application,
    ConversationHandler,
    CallbackQueryHandler
)
from dotenv import load_dotenv

from gemini_pro_bot.filters import AuthorizedUserFilter
from gemini_pro_bot.handlers import (
    start,
    help_command,
    newchat_command,
    handle_message,
    handle_image,
    handle_voice,
    handle_feedback_button,
    broadcast_message,
    get_message_type,
    broadcast_cancel,
    broadcast_start,
    BROADCAST_MESSAGE, 
    MESSAGE_TYPE
)

load_dotenv()

# Database connection
DATABASE_FILE = 'user_database.db'

async def init_db():
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE
    )
        ''')
        await db.commit()
        
broadcast_handler = ConversationHandler(
    entry_points=[CommandHandler('broadcast', broadcast_start)],
    states={
        BROADCAST_MESSAGE: [MessageHandler(filters.ALL & ~filters.COMMAND, get_message_type)],
        MESSAGE_TYPE: [MessageHandler(filters.ALL & ~filters.COMMAND, broadcast_message)],
    },
    fallbacks=[CommandHandler('cancel', broadcast_cancel)],
)
def start_bot() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("BOT_TOKEN")).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start, filters=AuthorizedUserFilter()))
    application.add_handler(CommandHandler("help", help_command, filters=AuthorizedUserFilter()))
    application.add_handler(CommandHandler("new", newchat_command, filters=AuthorizedUserFilter()))
    application.add_handler(broadcast_handler)

    # Any text message is sent to LLM to generate a response
    application.add_handler(
        MessageHandler( AuthorizedUserFilter() & ~filters.COMMAND & filters.TEXT, handle_message)
    )

    # Any image is sent to LLM to generate a response
    application.add_handler(
        MessageHandler( AuthorizedUserFilter() & ~filters.COMMAND & filters.PHOTO, handle_image)
    )

    application.add_handler(
        MessageHandler( AuthorizedUserFilter() & ~filters.COMMAND & filters.VOICE, handle_voice)
    )
    
    application.add_handler(CallbackQueryHandler(handle_feedback_button))

    # Initialize the database when the bot starts
    asyncio.get_event_loop().run_until_complete(init_db())

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
