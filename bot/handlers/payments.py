import aiohttp
from aiogram.types import Message, ContentType, PreCheckoutQuery

from bot.loader import dp, bot, config, accessor


@dp.message_handler(content_types='web_app_data')
async def buy_process(web_app_message: Message):
    async with aiohttp.ClientSession() as client:
        products = await accessor.get_products(client)
    product_id = int(web_app_message.web_app_data.data)
    product = next(
        (product for product in products if product.id == product_id), None)

    await bot.send_invoice(
        chat_id=web_app_message.chat.id,
        title=product.title,
        description=product.description,
        provider_token=config.telegram.payment_token,
        currency='rub',
        need_name=True,
        need_phone_number=True,
        need_shipping_address=True,
        prices=product.price,
        start_parameter='order',
        payload='order_invoice',
    )


@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    await message.answer(text='Платеж успешно совершен! Ожидайте заказ.')
