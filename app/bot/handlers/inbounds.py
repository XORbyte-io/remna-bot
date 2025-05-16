from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from app.api.client import RemnawaveAPIClient
from app.config import Config
from app.logger import setup_logger

def register_inbound_handlers(dp: Dispatcher):
    logger = setup_logger()
    client = RemnawaveAPIClient()

    @dp.message_handler(Text(equals="Inbounds"))
    async def inbounds_menu(message: types.Message):
        if message.from_user.id != Config.ADMIN_ID:
            await message.answer("Access denied.")
            return
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("List Inbounds", callback_data="list_inbounds"),
            types.InlineKeyboardButton("Add to Users", callback_data="add_inbound_users")
        )
        await message.answer("Select an action:", reply_markup=keyboard)

    @dp.callback_query_handler(text="list_inbounds")
    async def list_inbounds(callback: types.CallbackQuery):
        if callback.from_user.id != Config.ADMIN_ID:
            await callback.answer("Access denied.")
            return
        inbounds_data = client.get_inbounds()
        inbounds = inbounds_data['response']
        response = "Inbounds:\n"
        for inbound in inbounds[:5]:  # Limit to 5 for brevity
            response += f"Tag: {inbound['tag']}, Type: {inbound['type']}, UUID: {inbound['uuid']}\n"
        await callback.message.answer(response)

    @dp.callback_query_handler(text="add_inbound_users")
    async def add_inbound_to_users(callback: types.CallbackQuery):
        if callback.from_user.id != Config.ADMIN_ID:
            await callback.answer("Access denied.")
            return
        await callback.message.answer("Enter inbound UUID to add to users:")
        dp.register_message_handler(add_inbound_to_users_handler, content_types=types.ContentTypes.TEXT)

    async def add_inbound_to_users_handler(message: types.Message):
        if message.from_user.id != Config.ADMIN_ID:
            await message.answer("Access denied.")
            return
        inbound_uuid = message.text
        try:
            client.add_inbound_to_users(inbound_uuid)
            await message.answer("Inbound added to users successfully.")
            logger.info(f"Inbound {inbound_uuid} added to users by admin {message.from_user.id}")
        except Exception as e:
            await message.answer(f"Error adding inbound: {str(e)}")
            logger.error(f"Error adding inbound {inbound_uuid}: {str(e)}")
        dp.message_handlers.unregister(add_inbound_to_users_handler)
