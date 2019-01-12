import json

from behave import given, when, then


@given('an account {account_number} has balance {amount}')
def create_account(context, account_number, amount):
    context.accounts.add({
        'accountNumber': account_number,
        'accountState': 'active'
    })


@given('there is not account with the number {account_number}')
def do_not_create_account(context, account_number):
    pass  # Intentional no-op


@when('an account {account_number} is credited with {amount}')
def credit_account(context, account_number, amount):
    context.events_in.produce({
        'accountNumber': account_number,
        'amount': amount
    })


@then('a account {account_number} should have a balance of {balance:d}')
def assert_account_balance(context, account_number, balance):
    published_event = json.loads(context.events_out.last_event)
    expected_event = {'accountNumber': account_number, 'balance': balance}
    assert published_event == expected_event, \
        f'{repr(published_event)} != {repr(expected_event)}'


@then('a bad transaction should be reported')
def assert_bad_transaction(context):
    published_event = context.events_out.last_event
    assert published_event is None
