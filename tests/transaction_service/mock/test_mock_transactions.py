import pytest

from transaction_service.mock.mock_transactions import MockTransactions


@pytest.fixture(scope='function')
def transactions():
    return MockTransactions()


def test_fetch_by_account_number_when_no_transactions(transactions):
    assert transactions.fetch_by_account_number('1234') == []


def test_fetch_by_account_number_returns_the_transactions(transactions):
    account_a = '1234'
    account_b = '4567'
    transactions.store({'accountNumber': account_a, 'amount': 10})
    transactions.store({'accountNumber': account_b, 'amount': 20})
    transactions.store({'accountNumber': account_a, 'amount': 30})

    assert transactions.fetch_by_account_number(account_a) == [
        {'accountNumber': account_a, 'amount': 10},
        {'accountNumber': account_a, 'amount': 30}
    ]
