from transaction_service.app import Application
from transaction_service.mock.mock_events import MockEvents

def before_all(context):
    context.events_in = MockEvents()
	context.events_out = MockEvents()

	context.app = Application(consumer=events_in, publisher=events_out)
	context.app.start()