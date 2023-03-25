from aiogram.types import InlineKeyboardMarkup, WebAppInfo, InlineKeyboardButton

from bot.loader import config

web_app = WebAppInfo(url=f"{config.web_info.webapp_url}/")

web_app_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
web_app_keyboard.add(InlineKeyboardButton(text="Оформить заказ", web_app=web_app))
