import aiohttp
from aiohttp.web import json_response

from bot.loader import bot, config, accessor, dp
from bot.views.view import View
from utils.schemas import Product


class InvoiceLinkView(View):
    async def post(self):
        data = await self.request.json()
        request_product = Product.from_dict(data["product"])
        user_id = data["user_id"]
        if not request_product:
            return json_response(
                status=400,
                reason="Bad request",
            )
        async with aiohttp.ClientSession() as client:
            db_products = await accessor.get_products(client)
        if db_products is None:
            return json_response(
                status=500,
                reason="Internal Server Error",
            )
        product = next(
            (product for product in db_products if product == request_product), None
        )
        if not product:
            return json_response(
                status=404,
                reason="Product not found",
            )
        await dp.storage.set_data(user=user_id, data=product)
        invoice_link = await bot.create_invoice_link(
            title=product.title,
            description=product.description if product.description else product.title,
            provider_token=config.telegram.payment_token,
            currency="rub",
            prices=product.price,
            need_name=True,
            need_phone_number=True,
            need_shipping_address=True,
            payload="order_invoice",
        )
        return json_response(data={"invoice_link": invoice_link})
