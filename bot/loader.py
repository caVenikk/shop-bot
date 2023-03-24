import aiohttp_cors
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp import web

from utils import Config
from utils.accessor import Accessor

config = Config.load()
accessor = Accessor()
memory_storage = MemoryStorage()
bot = Bot(token=config.telegram.bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage=memory_storage)
app = web.Application()

cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True, expose_headers="*", allow_headers="*"
        )
    },
)

for route in list(app.router.routes()):
    cors.add(route)
