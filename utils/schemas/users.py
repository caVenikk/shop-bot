from dataclasses import dataclass


@dataclass
class User:
    id: int
    first_name: str
    second_name: str | None = None
    username: str | None = None

    def to_dict(self):
        return dict(
            id=self.id,
            first_name=self.first_name,
            second_name=self.second_name,
            username=self.username,
        )
