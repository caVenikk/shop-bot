import os
from dataclasses import dataclass
from typing import ClassVar, Optional


@dataclass
class WebInfo:
    api_url: str
    webapp_url: str


@dataclass
class Telegram:
    bot_token: str
    payment_token: str


@dataclass
class Config:
    web_info: WebInfo | None = None
    telegram: Telegram | None = None
    _config: ClassVar[Optional["Config"]] = None

    @classmethod
    def load(cls):
        if cls._config:
            return cls._config
        if os.path.exists('.env'):
            from dotenv import load_dotenv
            load_dotenv()
        try:
            cls._config = cls(
                web_info=WebInfo(
                    api_url=os.environ['API_URL'],
                    webapp_url=os.environ['WEBAPP_URL'],
                ),
                telegram=Telegram(
                    bot_token=os.environ['BOT_TOKEN'],
                    payment_token=os.environ['PAYMENT_TOKEN'],
                )
            )
        except KeyError:
            raise Exception("Environment variables does not exists.")
        return cls._config
