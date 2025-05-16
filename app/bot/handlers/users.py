from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from app.api.client import RemnawaveAPIClient
from app.config import Config
from app.logger import setup_logger

def register_user_handlers(dp: Dispatcher):
    logger = setup_logger()
    client = RemnawaveAPIClient()

    @dp.message_handler(Text(equals="Users"))
    async def users_menu(message: types.Message):
        if message.from_user.id != Config.ADMIN_ID:
            await message.answer("Access denied.")
            return
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("List Users", callback_data="list_users"),
            types.InlineKeyboardButton("Search User", callback_data="search_user")
        )
        await message.answer("Select an action:", reply_markup=keyboard)

    @dp.callback_query_handler(text="list_users")
    async def list_users(callback: types.CallbackQuery):
        if callback.from_user.id != Config.ADMIN_ID:
            await callback.answer("Access denied.")
            return
        users_data = client.get_users()
        users = users_data['response']['users']
        response = "Users:\n"
        for user in users[:5]:  # Limit to 5 for brevity
            response += f"Username: {user['username']}, Status: {user['status']}, UUID: {user['uuid']}\n"
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Next Page", callback_data="next_page_users"))
        await callback.message.answer(response, reply_markup=keyboard)

    @dp.callback_query_handler(text="search_user")
    async def search_user(callback: types.CallbackQuery):
        if callback.from_user.id != Config.ADMIN_ID:
            await callback.answer("Access denied.")
            return
        await callback.message.answer("Enter username to search:")
        dp.register_message_handler(search_user_by_username, content_types=types.ContentTypes.TEXT)

    async def search_user_by_username(message: types.Message):
        if message.from_user.id != Config.ADMIN_ID:
            await message.answer("Access denied.")
            return
        username = message.text
        try:
            user_data = client.get_user_by_username(username)
            user = user_data['response']['user']
            response = (
                f"Username: {user['username']}\n"
                f"Status: {user['userStatus']}\n"
                f"Traffic Used: {user['trafficUsed']}\n"
                f"Expires At: {user['expiresAt']}"
            )
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton("Disable", callback_data=f"disable_user_{user['shortUuid']}"),
                types.InlineKeyboardButton("Reset Traffic", callback_data=f"reset_traffic_{user['shortUuid']}")
            )
            await message.answer(response, reply_markup=keyboard)
        except Exception as e:
            await message.answer(f"User not found or error: {str(e)}")
            logger.error(f"Error searching user {username}: {str(e)}")
        dp.message_handlers.unregister(search_user_by_username)

    @dp.callback_query_handler(lambda c: c.data.startswith("disable_user_"))
    async def disable_user(callback: types.CallbackQuery):
        if callback.from_user.id != Config.ADMIN_ID:
            await callback.answer("Access denied.")
            return
        user_uuid = callback.data.split("_")[-1]
        try:
            client.disable_user(user_uuid)
            await callback.message.answer("User disabled successfully.")
            logger.info(f"User {user_uuid} disabled by admin {callback.from_user.id}")
        except Exception as e:
            await callback.message.answer(f"Error disabling user: {str(e)}")
            logger.error(f"Error disabling user {user_uuid}: {str(e)}")

    @dp.callback_query_handler(lambda c: c.data.startswith("reset_traffic_"))
    async def reset_traffic(callback: types.CallbackQuery):
        if callback.from_user.id != Config.ADMIN_ID:
            await callback.answer("Access denied.")
            return
        user_uuid = callback.data.split("_")[-1]
        try:
            client.reset_traffic(user_uuid)
            await callback.message.answer("Traffic reset successfully.")
            logger.info(f"Traffic reset for user {user_uuid} by admin {callback.from_user.id}")
        except Exception as e:
            await callback.message.answer(f"Error resetting traffic: {str(e)}")
            logger.error(f"Error resetting traffic for user {user_uuid}: {str(e)}")
