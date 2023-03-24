import aiohttp
from aiogram.types import Message

from bot.loader import dp, bot, accessor
from bot.markups.reply import web_app_keyboard
from utils.schemas.users import User


@dp.message_handler(commands=["start", "order"], state="*")
async def start_handler(message: Message):
    user = User(
        id=message.from_user.id,
        first_name=message.from_user.first_name,
        second_name=message.from_user.last_name,
        username=message.from_user.username,
    )
    async with aiohttp.ClientSession() as client:
        await accessor.add_user(client, user)

    text = "Приступим к заказу! 🍟\nНажмите на кнопку ниже или в меню, чтобы заказать идеальный обед! 🌯"
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=web_app_keyboard,
    )
