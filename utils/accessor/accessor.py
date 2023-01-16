from utils import Config
from utils.schemas import Product


class Accessor:
    def __init__(self):
        self._config = Config.load()

    async def get_products(self, client):
        async with client.get(f"{self._config.web_info.api_url}/products") as resp:
            assert resp.status == 200
            result_json = await resp.json()
            products = [Product(**product) for product in result_json]
            return products
