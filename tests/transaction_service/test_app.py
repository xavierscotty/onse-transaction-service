from unittest.mock import Mock

import pytest

from transaction_service.app import Application
from transaction_service.mock.mock_events import MockEvents
from transaction_service.mock.mock_transactions import MockTransactionClient


@pytest.fixture(scope='function')
def app(logger):
    application = Application(transaction_events=MockEvents(),
                              balance_updates=MockEvents(),
                              accounts_client=Mock(),
                              transaction_repository=MockTransactionClient(),
                              logger=logger)
    application.start()
    return application


@pytest.fixture(scope='function')
def logger():
    return Mock()


def test_a_message_is_logged_on_event(app, logger):
    event = {'accountNumber': '1234', 'amount': '99'}
    app.transaction_events.produce(event)
    logger.debug.assert_called_with('Received transaction event',
                                    received_event=event)


def test_the_app_checks_if_the_account_exists(app):
    app.transaction_events.produce({'accountNumber': '1234', 'amount': '99'})
    app.accounts_client.has_active_account.assert_called()


def test_successful_transaction(app, logger):
    app.transaction_repository.store({'accountNumber': '1234', 'amount': 100})
    app.transaction_events.produce({'accountNumber': '1234', 'amount': '99'})
    expected_event = '{"accountNumber": "1234", "balance": 199}'
    assert app.balance_updates.last_event == expected_event
    logger.info.assert_called_with('Successful transaction',
                                   account_number='1234',
                                   amount=99,
                                   balance=199)


def test_transaction_when_account_is_not_active(app, logger):
    app.accounts_client.has_active_account.return_value = False
    app.transaction_events.produce({'accountNumber': '1234', 'amount': '99'})
    assert app.balance_updates.last_event is None
    logger.warning.assert_called_with('Attempted transaction against inactive '
                                      'account',
                                      account_number='1234',
                                      amount=99)
