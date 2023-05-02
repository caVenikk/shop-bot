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
            user_id = data["user_id"]
        except KeyError:
            return json_response(
                status=402,
                reason="Unprocessable Entity",
            )
        if not request_products:
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
        await dp.storage.set_data(user=user_id, data=products)
        invoice_link = await bot.create_invoice_link(
            title=f"Заказ #{last_order_id}",
            description="Идеальный обед с McBonald's",
            photo_url="https://hips.hearstapps.com/hmg-prod/images/190130-chicken-shwarma-horizontal-1549421250.png?crop=1xw:0.843328335832084xh;center,top",
            provider_token=config.telegram.payment_token,
            currency="rub",
            prices=[product.price for product in products],
            need_name=True,
            need_phone_number=True,
            need_shipping_address=True,
            payload="order_invoice",
        )
        return json_response(data={"invoice_link": invoice_link})
