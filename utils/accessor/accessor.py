from utils import Config
from utils.schemas import Product, Order


class Accessor:
    def __init__(self):
        self._config = Config.load()

    async def get_products(self, client):
        async with client.get(f"{self._config.web_info.api_url}/products") as resp:
            assert resp.status == 200
            result_json = await resp.json()
            products = [Product(**product) for product in result_json]
            return products

    async def add_order(self, client, order: Order):
        async with client.post(
            f"{self._config.web_info.api_url}/orders", json=order.to_dict()
        ) as resp:
            assert resp.status == 201
            result_json = await resp.json()
            return result_json
