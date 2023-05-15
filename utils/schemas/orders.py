from dataclasses import dataclass


@dataclass
class Order:
    user_id: int
    products_ids: list[int]
    counters: list[int]
    name: str
    phone_number: str
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str
    total_amount: int

    def to_dict(self):
        return dict(
            user_id=self.user_id,
            products_ids=self.products_ids,
            counters=self.counters,
            name=self.name,
            phone_number=self.phone_number,
            country_code=self.country_code,
            state=self.state,
            city=self.city,
            street_line1=self.street_line1,
            street_line2=self.street_line2,
            post_code=self.post_code,
            total_amount=self.total_amount,
        )
