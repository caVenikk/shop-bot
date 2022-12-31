from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils.accessor import Accessor
from utils.config import Config

config = Config.load()
accessor = Accessor()
memory_storage = MemoryStorage()
bot = Bot(token=config.telegram.bot_token, parse_mode='HTML')
dp = Dispatcher(bot, storage=memory_storage)
