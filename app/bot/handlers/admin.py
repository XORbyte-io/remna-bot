from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import CommandStart, Command
from app.config import Config
from app.logger import setup_logger

def register_admin_handlers(dp: Dispatcher):
    logger = setup_logger()

    @dp.message_handler(CommandStart())
    async def start_command(message: types.Message):
        if message.from_user.id != Config.ADMIN_ID:
            await message.answer("Access denied. You are not authorized.")
            logger.warning(f"Unauthorized access attempt by user {message.from_user.id}")
            return
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Users", "Inbounds", "Stats")
        await message.answer("Welcome to Remnawave VPN Bot!", reply_markup=keyboard)
        logger.info(f"Admin {message.from_user.id} started the bot")
