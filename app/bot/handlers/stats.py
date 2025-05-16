from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from app.api.client import RemnawaveAPIClient
from app.config import Config
from app.logger import setup_logger

def register_stats_handlers(dp: Dispatcher):
    logger = setup_logger()
    client = RemnawaveAPIClient()

    @dp.message_handler(Text(equals="Stats"))
    async def stats_menu(message: types.Message):
        if message.from_user.id != Config.ADMIN_ID:
            await message.answer("Access denied.")
            return
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("System Stats", callback_data="system_stats"),
            types.InlineKeyboardButton("Nodes Stats", callback_data="nodes_stats")
        )
        await message.answer("Select an action:", reply_markup=keyboard)

    @dp.callback_query_handler(text="system_stats")
    async def system_stats(callback: types.CallbackQuery):
        if callback.from_user.id != Config.ADMIN_ID:
            await callback.answer("Access denied.")
            return
        stats = client.get_system_stats()['response']
        response = (
            f"System Stats:\n"
            f"CPU Cores: {stats['cpu']['cores']}\n"
            f"Memory Used: {stats['memory']['used']} bytes\n"
            f"Total Users: {stats['users']['totalUsers']}\n"
            f"Uptime: {stats['uptime']} seconds"
        )
        await callback.message.answer(response)

    @dp.callback_query_handler(text="nodes_stats")
    async def nodes_stats(callback: types.CallbackQuery):
        if callback.from_user.id != Config.ADMIN_ID:
            await callback.answer("Access denied.")
            return
        stats = client.get_nodes_stats()['response']['lastSevenDays']
        response = "Nodes Stats (Last 7 Days):\n"
        for stat in stats[:5]:  # Limit to 5 for brevity
            response += f"Node: {stat['nodeName']}, Total Bytes: {stat['totalBytes']}, Date: {stat['date']}\n"
        await callback.message.answer(response)
