from pika import ConnectionParameters, BlockingConnection
import sys
import os
from transaction_service.rabbitevents import RabbitProducer

properties = {
    'exchange': 'transactions',
    'queue': 'transactions',
    'host': os.getenv('RABBITMQ_HOST', 'localhost')
}
producer = RabbitProducer(properties)

producer.publish(sys.argv[1])
