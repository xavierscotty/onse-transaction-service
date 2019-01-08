import logging

from structlog import wrap_logger

from transaction_service.app import Application
from transaction_service.mock.mock_events import MockEvents
from transaction_service.mock.mock_accounts import MockAccounts
from transaction_service.mock.mock_transactions import MockTransactions


def before_scenario(context, scenario):
    context.events_in = MockEvents()
    context.events_out = MockEvents()

    context.accounts = MockAccounts()

    logger = logging.getLogger()
    logger.addHandler(logging.NullHandler())

    context.app = Application(consumer=context.events_in,
                              producer=context.events_out,
                              accounts=context.accounts,
                              transactions=MockTransactions(),
                              logger=wrap_logger(logger))
    context.app.start()
