import aiohttp
from aiogram.types import Message

from bot.loader import dp, bot, accessor
from bot.markups.reply import web_app_keyboard


@dp.message_handler(commands=['start', 'order'], state='*')
async def start_handler(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text='Оформите заказ, нажав на кнопку ниже!',
        reply_markup=web_app_keyboard
    )
    async with aiohttp.ClientSession() as client:
        data = {"products": await accessor.get_products(client)}
        await dp.storage.set_data(
            chat=message.chat.id,
            user=message.from_user.id,
            data=data
        )
