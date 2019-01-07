from transaction_service.app import Application
from transaction_service.mock.mock_events import MockEvents

def before_all(context):
	context.events_in = MockEvents()
	context.events_out = MockEvents()

	context.app = Application(consumer=context.events_in,
							  producer=context.events_out)
	context.app.start()