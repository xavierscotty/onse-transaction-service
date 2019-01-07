import json

class Application:
    def __init__(self, consumer, producer, accounts):
        self.consumer = consumer
        self.producer = producer
        self.accounts = accounts

    def start(self):
        self.consumer.on_event(self.handle_event)

    def handle_event(self, event):
        print('handling event')
        account_exists = self.accounts.has_active_account(event['accountNumber'])

        if not account_exists:
            print("Invalid account")
            return

        print(event)

        self.producer.publish(json.dumps(
            {'accountNumber': event['accountNumber'], 'balance': 10}))
