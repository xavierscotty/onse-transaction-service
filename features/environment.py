from transaction_service.app import Application
from transaction_service.mock.mock_events import MockEvents
from transaction_service.mock.mock_accounts import MockAccounts


def before_scenario(context, scenario):
    context.events_in = MockEvents()
    context.events_out = MockEvents()

    context.accounts = MockAccounts()

    context.app = Application(consumer=context.events_in,
                              producer=context.events_out,
                              accounts=context.accounts)
    context.app.start()
