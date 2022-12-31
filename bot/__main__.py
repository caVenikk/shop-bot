from aiogram.utils.executor import start_polling, Dispatcher
from loguru import logger

from bot.handlers import dp


def on_events():
    async def startup(_: Dispatcher) -> None:
        pass

    async def shutdown(dispatcher: Dispatcher) -> None:
        logger.info("Closing storage...")
        await dispatcher.storage.close()
        await dispatcher.storage.wait_closed()
        logger.info("Bot shutdown...")

    return startup, shutdown


if __name__ == '__main__':
    logger.info(f"Number of message handlers: {len(dp.message_handlers.handlers)}.")
    logger.info(f"Number of callback query handlers: {len(dp.callback_query_handlers.handlers)}.")
    on_startup, on_shutdown = on_events()
    start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )
