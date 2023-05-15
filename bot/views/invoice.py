from json import JSONDecodeError

import aiohttp
from aiohttp.web import json_response

from bot.loader import bot, config, accessor, dp
from bot.views.view import View
from utils.schemas import Product


class InvoiceLinkView(View):
    async def post(self):
        try:
            data = await self.request.json()
        except JSONDecodeError:
            return json_response(
                status=400,
                reason="Bad request",
            )
        try:
            request_products = [Product.from_dict(product) for product in data["products"]]
            counters = [int(value) for value in data["counters"]]
            user_id = data["user_id"]
        except KeyError:
            return json_response(
                status=402,
                reason="Unprocessable Entity",
            )
        if not request_products or not counters:
            return json_response(
                status=400,
                reason="Bad request",
            )
        async with aiohttp.ClientSession() as client:
            db_products = await accessor.get_products(client)
            last_order_id = await accessor.get_last_order_id(client)
        if db_products is None:
            return json_response(
                status=500,
                reason="Internal Server Error",
            )
        products = []
        for req_product in request_products:
            product = next((db_product for db_product in db_products if db_product == req_product), None)
            if not product:
                return json_response(
                    status=404,
                    reason="Product not found",
                )
            products.append(product)
        for product, counter in zip(products, counters):
            product.counter = counter
        await dp.storage.set_data(user=user_id, data=dict(products=products, counters=counters))
        invoice_link = await bot.create_invoice_link(
            title=f"Заказ #{last_order_id + 1}",
            description="Идеальный обед с McBonald's",
            photo_url="https://t.ly/oODG",
            provider_token=config.telegram.payment_token,
            currency="rub",
            prices=[product.labeled_price for product in products],
            need_name=True,
            need_phone_number=True,
            need_shipping_address=True,
            payload="order_invoice",
        )
        return json_response(data={"invoice_link": invoice_link})
