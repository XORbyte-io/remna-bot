from flask import Flask
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.config import Config
from app.bot.handlers.admin import register_admin_handlers
from app.bot.handlers.users import register_user_handlers
from app.bot.handlers.inbounds import register_inbound_handlers
from app.bot.handlers.stats import register_stats_handlers
from app.logger import setup_logger
import asyncio
import logging

app = Flask(__name__)
logger = setup_logger()

# Initialize bot
config = Config()
bot = Bot(token=config.TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Register handlers
register_admin_handlers(dp)
register_user_handlers(dp)
register_inbound_handlers(dp)
register_stats_handlers(dp)

@app.route('/')
def index():
    return {"status": "Remnawave Bot is running"}

async def on_startup():
    logger.info("Starting bot...")
    webhook_url = f"{config.WEBHOOK_URL}/webhook"
    await bot.set_webhook(webhook_url)
    logger.info("Webhook set")

if __name__ == '__main__':
    # Start polling in development
    if config.ENV == 'development':
        asyncio.run(dp.start_polling())
    else:
        # In production, Flask handles webhook
        app.run(host='0.0.0.0', port=8000)
