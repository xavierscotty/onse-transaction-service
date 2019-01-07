from transaction_service.accounts_rest_client import AccountsRestClient
import pytest
import requests_mock

@pytest.fixture(scope="function")
def rest_client():
    rest_client = AccountsRestClient(url='http://accounts.service')
    return rest_client


def test_has_account_with_number_not_exists(rest_client):
    with requests_mock.mock() as m:
        m.get('http://accounts.service/accounts/23423234',
              json={"message": "Not Found"},
              status_code=404)
        assert rest_client.has_active_account('23423234') is False


def test_has_active_account(rest_client):
    with requests_mock.mock() as m:
        account_number = '99887866'
        m.get(f'http://accounts.service/accounts/{account_number}',
              json={
                  'accountNumber': account_number,
                  'accountStatus': 'active'
              },
              status_code=200)
        assert rest_client.has_active_account(account_number) is True


def test_has_closed_account(rest_client):
    with requests_mock.mock() as m:
        account_number = '99887866'
        m.get(f'http://accounts.service/accounts/{account_number}',
              json={
                  'accountNumber': account_number,
                  'accountStatus': 'closed'
              },
              status_code=200)
        assert rest_client.has_active_account(account_number) is False


