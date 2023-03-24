import aiohttp
from aiogram.types import Message, ContentType, PreCheckoutQuery

from bot.loader import dp, bot, accessor
from utils.schemas import Order


@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    product = await dp.storage.get_data(user=message.from_user.id)
    total_amount = message.successful_payment.total_amount
    shipping_address = dict(message.successful_payment.order_info.shipping_address)
    order = Order(
        user_id=message.from_user.id,
        product_id=product.id,
        total_amount=total_amount,
        name=message.successful_payment.order_info.name,
        phone_number=message.successful_payment.order_info.phone_number,
        **shipping_address,
    )
    async with aiohttp.ClientSession() as client:
        await accessor.add_order(client, order)

    await message.answer(text="Платеж успешно совершен! Ожидайте заказ.")
