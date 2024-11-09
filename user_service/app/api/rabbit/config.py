import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    RABBIT_HOST: str = os.getenv("RABBIT_HOST", default="rabbitmq")
    RABBIT_USER: str = os.getenv("RABBIT_USER", default="user")
    RABBIT_PASSWORD: str = os.getenv("RABBIT_PASSWORD", default="pass")
    ORDER_QUEUE: str = os.getenv("ORDER_QUEUE", default="order_queue")


config = Config()
