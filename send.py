import sys
import os
from transaction_service.infrastructure.rabbit_events import RabbitProducer

properties = {
    'exchange': 'transactions',
    'queue': 'transactions',
    'host': os.getenv('RABBITMQ_HOST', 'localhost')
}
producer = RabbitProducer(properties)

producer.produce(sys.argv[1])
