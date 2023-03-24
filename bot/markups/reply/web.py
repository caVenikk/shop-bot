from aiogram.types import ReplyKeyboardMarkup, WebAppInfo, KeyboardButton

from bot.loader import config

web_app = WebAppInfo(url=f"{config.web_info.webapp_url}/")

web_app_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Оформить заказ", web_app=web_app)]],
    resize_keyboard=True,
)
