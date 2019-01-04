class Application:
	def __init__(self, consumer, producer):
		self.consumer = consumer
		self.producer = producer

	def start(self):
		self.consumer.on_event(self.handle_event)

	def handle_event(event):
		self.producer.publish({"accountId": 1234, "balance": 10})
