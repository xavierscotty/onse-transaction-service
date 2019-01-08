import os

import structlog

from transaction_service.app import Application
from transaction_service.infrastructure.accounts_rest_client import \
    AccountsRestClient
from transaction_service.infrastructure.rabbit_events import RabbitConsumer, \
    RabbitProducer
from transaction_service.mock.mock_transactions import MockTransactions

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
                      transactions=MockTransactions())

    app.start()
