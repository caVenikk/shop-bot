import asyncio

import nest_asyncio
from aiogram.utils.executor import start_polling, Dispatcher
from aiohttp import web
from loguru import logger

from bot.handlers import dp
from bot.loader import app
from bot.views.invoice import InvoiceLinkView

nest_asyncio.apply()


def on_events():
    async def startup(_: Dispatcher) -> None:
        pass

    async def shutdown(dispatcher: Dispatcher) -> None:
        logger.info("Closing storage...")
        await dispatcher.storage.close()
        await dispatcher.storage.wait_closed()
        logger.info("Bot shutdown...")

    return startup, shutdown


async def main():
    app.router.add_view("/create_invoice_link", InvoiceLinkView)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 8888)
    await site.start()
    logger.info(f"Web app is running on {site.name}")

    logger.info(f"Number of message handlers: {len(dp.message_handlers.handlers)}.")
    logger.info(
        f"Number of callback query handlers: {len(dp.callback_query_handlers.handlers)}."
    )
    on_startup, on_shutdown = on_events()
    start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )


if __name__ == "__main__":
    asyncio.run(main())
