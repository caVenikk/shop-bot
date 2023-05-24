from dataclasses import dataclass

from aiogram.types import LabeledPrice


@dataclass
class Product:
    id: int
    title: str
    price: int
    active: bool
    counter: int | None = None
    weight: float | None = None
    description: str | None = None

    @property
    def labeled_price(self):
        return LabeledPrice(label=f"{self.title} x{self.counter}", amount=int(self.price * self.counter * 100))

    @classmethod
    def from_dict(cls, product: dict, **_):
        return cls(**product)
