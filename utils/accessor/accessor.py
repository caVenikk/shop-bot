from utils import Config
from utils.schemas import Product, Order
from utils.schemas.users import User


class Accessor:
    def __init__(self):
        self._config = Config.load()

    async def get_products(self, client):
        async with client.get(f"{self._config.web_info.api_url}/products") as resp:
            assert resp.status == 200
            result_json = await resp.json()
            products = [Product(**product) for product in result_json]
            return products

    async def get_user(self, client, user_id):
        async with client.get(f"{self._config.web_info.api_url}/users/{user_id}") as resp:
            assert resp.status == 200
            user = await resp.json()
            return User(**user)

    async def update_user(self, client, user):
        async with client.put(
                f"{self._config.web_info.api_url}/users", json=user.to_dict()
        ) as resp:
            assert resp.status == 200
            user = await resp.json()
            return user

    async def add_user(self, client, user):
        db_user = await self.get_user(client, user.id)
        if db_user:
            await self.update_user(client, user)
            return db_user
        async with client.post(
                f"{self._config.web_info.api_url}/users", json=user.to_dict()
        ) as resp:
            assert resp.status == 201
            user = await resp.json()
            return user

    async def add_order(self, client, order: Order):
        async with client.post(
                f"{self._config.web_info.api_url}/orders", json=order.to_dict()
        ) as resp:
            assert resp.status == 201
            order = await resp.json()
            return order
