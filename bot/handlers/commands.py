from aiogram.types import Message

from bot.loader import dp, bot
from bot.markups.reply import web_app_keyboard


@dp.message_handler(commands=['start', 'order'], state='*')
async def start_handler(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text='Оформите заказ, нажав на кнопку ниже!',
        reply_markup=web_app_keyboard
    )
