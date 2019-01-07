
import os
from transaction_service.app import Application
from transaction_service.rabbitevents import RabbitConsumer, RabbitProducer


if __name__ == "__main__":
	consumer  = RabbitConsumer(exchange = 'test-consumer', queue= 'transaction_service_in')
	publisher = RabbitProducer(exchange = 'test-publisher',  queue='transaction_service_out')

	app = Application(consumer = consumer, producer = publisher)

	app.start()