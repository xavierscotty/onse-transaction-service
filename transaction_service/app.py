import json


class Application:
    def __init__(self, consumer, producer, accounts, logger,
                 transactions):
        self.consumer = consumer
        self.producer = producer
        self.accounts = accounts
        self.logger = logger
        self.transactions = transactions

    def start(self):
        self.consumer.on_event(self.handle_event)

    def handle_event(self, event):
        self.logger.debug('Received transaction event', received_event=event)

        account_number = event['accountNumber']
        amount = int(event['amount'])

        account_exists = self.accounts.has_active_account(account_number)

        if not account_exists:
            self.logger.warn(
                'Attempted transaction against inactive '
                'account',
                account_number=account_number,
                amount=amount)
            return

        self.transactions.store({'accountNumber': account_number, 'amount': amount})
        transactions = self.transactions.fetch_by_account_number(account_number)

        balance = sum([tx['amount'] for tx in transactions])

        self.producer.produce(json.dumps(
            {'accountNumber': account_number, 'balance': balance}))

        self.logger.info('Successful transaction',
                         account_number=account_number,
                         amount=amount)
