# @when(u'I fetch customer {id}')

# def step_impl(context, id):
#     response = context.web_client.get('/customers/{0}'.format(id))
#     context.response = response.get_json()

# @then(u'I should see customer "{expected_name}"')
# def step_impl(context, expected_name):
#     full_name = context.response['firstName'] + " " + context.response['surname']
#     assert full_name == expected_name


@given(u'an account {account_id} has balance {amount}')
def step_impl(context):
    pass

@when(u'an account {account_id} is credited with {amount}')
def step_impl(context, account_id, amount):
    context.events_in.publish({
        'accountId': account_id,
        'amount': amount
    })

@then(u'a account {account_id} should have a balance of {balance}')
def step_impl(context, account_id, balance):
    assert context.events_out.last_event() == {'accountId': account_id, 'balance': balance}
