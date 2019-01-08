from behave import *
import json


@given(u'an account {account_number} has balance {amount}')
def step_impl(context, account_number, amount):
    context.accounts.add({
        'accountNumber': account_number,
        'accountState': 'active'
    })


@given(u'there is not account with the number {account_number}')
def step_impl(context, account_number):
    pass  # Intentional no-op


@when(u'an account {account_number} is credited with {amount}')
def step_impl(context, account_number, amount):
    context.events_in.produce({
        'accountNumber': account_number,
        'amount': amount
    })


@then(u'a account {account_number} should have a balance of {balance:d}')
def step_impl(context, account_number, balance):
    published_event = json.loads(context.events_out.last_event)
    expected_event = {'accountNumber': account_number, 'balance': balance}
    assert published_event == expected_event, f'{repr(published_event)} != {repr(expected_event)}'


@then(u'a bad transaction should be reported')
def step_impl(context):
    published_event = context.events_out.last_event
    assert published_event is None
