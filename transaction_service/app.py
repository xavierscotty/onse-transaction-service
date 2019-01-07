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

        print(type(event))

        account_number = '123123'
        account_exists = self.accounts.has_account_with_number(account_number)

        if not account_exists:
            print("Invalid account")
            return

        self.producer.publish(json.dumps(
            {'accountId': account_number, 'balance': 10}))
