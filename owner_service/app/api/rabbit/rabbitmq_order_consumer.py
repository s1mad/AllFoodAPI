import json
import logging
import os
import threading
import time

import pika
from pydantic import ValidationError

from app.api.rabbit.models import OrderRequest

# Получение параметров подключения к RabbitMQ из переменных окружения с дефолтными значениями
RABBIT_HOST: str = os.getenv("RABBIT_HOST", default="rabbitmq")
RABBIT_PORT: int = os.getenv("RABBIT_PORT", default=5672)
RABBIT_USER: str = os.getenv("RABBIT_USER", default="user")
RABBIT_PASSWORD: str = os.getenv("RABBIT_PASSWORD", default="pass")
ORDER_QUEUE: str = os.getenv("ORDER_QUEUE", default="order_queue")

# Список для хранения сообщений
orders = []


# Функция для запуска RabbitMQ-потребителя
def start_rabbitmq_order_consumer():
    """
    Запускает RabbitMQ-потребителя, который слушает очередь `ORDER_QUEUE` и обрабатывает полученные сообщения.

    Потребитель подключается к RabbitMQ серверу и начинает слушать очередь на предмет новых сообщений.
    Каждое сообщение, соответствующее модели `OrderRequest`, добавляется в список `orders`.
    В случае ошибок декодирования сообщения или валидации данных, выводится сообщение об ошибке в логах.
    """

    def main():
        """
       Основная функция потребителя RabbitMQ, которая пытается установить соединение с сервером RabbitMQ,
       затем слушает очередь и обрабатывает сообщения.

       Если подключение не удается, функция будет повторно пытаться подключиться каждые 1 секунду.
       Когда соединение установлено, создается канал и объявляется очередь для получения сообщений.
       """
        connection = None
        time.sleep(5)
        # Пытаемся подключиться к RabbitMQ до тех пор, пока соединение не будет установлено
        while connection is None:
            try:
                # Устанавливаем соединение с RabbitMQ
                connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host=RABBIT_HOST,
                    port=RABBIT_PORT,
                    credentials=pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
                ))
                logging.info("RabbitMQ connection established.")
            except pika.exceptions.AMQPConnectionError:
                # Если соединение не удается, выводим предупреждение и пробуем снова через 1 секунду
                logging.warning("RabbitMQ not available. Retrying in 1 seconds...")
                time.sleep(1)

        # Создаем канал для общения с RabbitMQ
        channel = connection.channel()

        # Объявляем очередь, если она не существует
        channel.queue_declare(queue=ORDER_QUEUE, durable=True)

        def callback(ch, method, properties, body):
            """
            Функция-обработчик для сообщений из очереди. Когда новое сообщение поступает в очередь,
            эта функция будет вызвана.
            """
            logging.info(f"RabbitMQ - {ORDER_QUEUE} - Get Message: {body}")
            try:
                # Декодируем сообщение из JSON
                message = json.loads(body)
                # Проверяем, соответствует ли сообщение модели OrderRequest
                order = OrderRequest(**message)
                # Если успешно, добавляем в массив orders
                orders.append(order.dict())
                logging.info("Message added to orders list.")
            except (json.JSONDecodeError, ValidationError) as e:
                # В случае ошибки декодирования или валидации выводим ошибку
                logging.error(f"Message format is invalid: {e}")

        # Настроим потребителя на получение сообщений из очереди
        channel.basic_consume(queue=ORDER_QUEUE, on_message_callback=callback, auto_ack=True)
        # Начинаем получать сообщения
        channel.start_consuming()

    # Запускаем функцию main в отдельном потоке, чтобы не блокировать основной поток приложения
    threading.Thread(target=main, daemon=True).start()
