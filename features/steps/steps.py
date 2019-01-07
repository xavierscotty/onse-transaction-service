# @when(u'I fetch customer {id}')

# def step_impl(context, id):
#     response = context.web_client.get('/customers/{0}'.format(id))
#     context.response = response.get_json()

# @then(u'I should see customer "{expected_name}"')
# def step_impl(context, expected_name):
#     full_name = context.response['firstName'] + " " + context.response['surname']
#     assert full_name == expected_name

@given(u'an account {account_id} has balance {amount}')
def step_impl(context, account_id, amount):
    pass

@when(u'an account {account_id} is credited with {amount}')
def step_impl(context, account_id, amount):
    context.events_in.publish({
        'accountId': account_id,
        'amount': amount
    })

@then(u'a account {account_id} should have a balance of {balance:d}')
def step_impl(context, account_id, balance):
    published_event = context.events_out.last_event
    expected_event  = {'accountId': account_id, 'balance': balance}

    assert published_event == expected_event, f'{repr(published_event)} != {repr(expected_event)}'
