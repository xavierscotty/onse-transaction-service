from transaction_service.mock.mock_accounts import MockAccounts
import pytest


@pytest.fixture(scope="function")
def accounts():
    accounts = MockAccounts()
    return accounts


def test_has_with_number_return_false_when_not_exists(accounts):
    accounts.add('9879020')
    assert accounts.has_account_with_number('2344234') is False


def test_has_with_number_return_true_when_exists(accounts):
    account_number = '31245987'
    accounts.add(account_number)
    assert accounts.has_account_with_number(account_number) is True
