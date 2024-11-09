import json
import logging

import pika

log = logging.getLogger(__name__)

class RabbitMQProducer:
    def __init__(self, host: str = "rabbitmq", order_queue: str = "order_queue", username: str = "user", password: str = "pass"):
        self.host = host
        self.order_queue = order_queue
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.order_queue, durable=True)

    def send_message(self, message: dict):
        """Отправка сообщения о заказе в RabbitMQ."""
        if not self.connection or self.connection.is_closed:
            self.connect()

        self.channel.basic_publish(
            exchange='',
            routing_key=self.order_queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )
        log.info("Order message sent to RabbitMQ.")

    def close_connection(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

rabbit_producer = RabbitMQProducer()

def init_rabbit_producer(host: str, order_queue: str, username: str, password: str):
    """Функция для инициализации RabbitMQProducer с заданными параметрами."""
    global rabbit_producer
    rabbit_producer = RabbitMQProducer(
        host=host,
        order_queue=order_queue,
        username=username,
        password=password
    )
    rabbit_producer.connect()
    log.info("RabbitMQ Producer успешно инициализирован")