from dataclasses import dataclass

from aiogram.types import LabeledPrice


@dataclass
class Product:
    id: int
    title: str
    price: int | list[LabeledPrice]
    weight: float | None = None
    description: str | None = None

    def __post_init__(self):
        self.price = [LabeledPrice(label=self.title, amount=int(self.price * 100))]

    @classmethod
    def from_dict(cls, product: dict):
        return cls(
            id=product["id"],
            title=product["title"],
            price=product["price"],
            weight=product["weight"],
            description=product["description"],
        )
