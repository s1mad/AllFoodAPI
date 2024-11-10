import json
import logging
import os
import time

import pika

RABBIT_HOST: str = os.getenv("RABBIT_HOST", default="rabbitmq")
RABBIT_USER: str = os.getenv("RABBIT_USER", default="user")
RABBIT_PASSWORD: str = os.getenv("RABBIT_PASSWORD", default="pass")
ORDER_QUEUE: str = os.getenv("ORDER_QUEUE", default="order_queue")


class RabbitMQProducer:
    """
    Класс для отправки сообщений в очередь RabbitMQ.

    Класс обеспечивает соединение с сервером RabbitMQ и отправку сообщений в указанную очередь.
    Соединение и канал создаются один раз при первом вызове, а при завершении можно закрыть соединение.
    """

    def __init__(self,
                 host: str = "rabbitmq",
                 order_queue: str = "order_queue",
                 username: str = "user",
                 password: str = "pass"):
        """
        Инициализирует объект RabbitMQProducer с параметрами подключения к RabbitMQ.
        """
        self.host = host
        self.order_queue = order_queue
        self.username = username
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        """Устанавливает соединение с RabbitMQ с поддержкой повторных попыток."""
        while self.connection is None:
            try:
                credentials = pika.PlainCredentials(self.username, self.password)
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, credentials=credentials))
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.order_queue, durable=True)
            except pika.exceptions.AMQPConnectionError as e:
                logging.warning(f"Failed to connect to RabbitMQ: {e}. Retrying in 1 seconds...")
                time.sleep(1)

    def send_message(self, message: dict):
        """
        Отправляет сообщение в очередь RabbitMQ.
        Если соединение отсутствует, оно будет установлено заново.
        """
        if not self.connection or self.connection.is_closed:
            self.connect()

        try:
            # Отправка сообщения
            self.channel.basic_publish(
                exchange='',
                routing_key=self.order_queue,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)  # Делает сообщение persistent
            )
            logging.info(f"Message sent to queue {self.order_queue}: {message}")
        except pika.exceptions.AMQPError as e:
            logging.error(f"Failed to send message to RabbitMQ: {e}")

    def close_connection(self):
        """Закрывает соединение с RabbitMQ, если оно активно."""
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logging.info("Connection to RabbitMQ closed.")


# Глобальная переменная для хранения экземпляра RabbitMQProducer
rabbit_producer = RabbitMQProducer()


def init_rabbit_producer():
    """
    Инициализирует глобальный объект RabbitMQProducer с заданными параметрами и подключается к серверу RabbitMQ.
    """
    global rabbit_producer
    rabbit_producer = RabbitMQProducer(
        host=RABBIT_HOST,
        order_queue=ORDER_QUEUE,
        username=RABBIT_USER,
        password=RABBIT_PASSWORD
    )
    rabbit_producer.connect()
    logging.info("RabbitMQProducer initialized and connected.")
