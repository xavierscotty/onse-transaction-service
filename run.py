import os

import structlog

from transaction_service.app import Application
from transaction_service.infrastructure.accounts_rest_client import \
    AccountsRestClient
from transaction_service.infrastructure.postgresql_transactions import \
    PostgreSQLTransactions
from transaction_service.infrastructure.rabbit_events import RabbitConsumer, \
    RabbitProducer

if __name__ == "__main__":
    consumer_properties = {
        'queue': 'transactions',
        'host': os.getenv('RABBITMQ_HOST', 'localhost')
    }
    producer_properties = {
        'exchange': 'balance_updates',
        'queue': 'balance_updates',
        'host': os.getenv('RABBITMQ_HOST', 'localhost')
    }
    consumer = RabbitConsumer(consumer_properties)
    publisher = RabbitProducer(producer_properties)
    accounts = AccountsRestClient(os.getenv('ACCOUNT_SERVICE_URL'))

    app = Application(consumer=consumer,
                      producer=publisher,
                      accounts=accounts,
                      logger=structlog.get_logger(),
                      transactions=PostgreSQLTransactions(
                          username=os.getenv('DB_USERNAME'),
                          password=os.getenv('DB_PASSWORD'),
                          host=os.getenv('DB_HOST'),
                          port=os.getenv('DB_PORT'),
                          db='transaction-service'))

    app.start()
