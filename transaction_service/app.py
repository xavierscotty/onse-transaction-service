import json


class Application:
    def __init__(self, transaction_events, balance_updates, accounts_client,
                 transaction_repository, logger):
        self.transaction_events = transaction_events
        self.balance_updates = balance_updates
        self.accounts_client = accounts_client
        self.transaction_repository = transaction_repository
        self.logger = logger

    def start(self):
        self.transaction_events.on_event(self.handle_event)

    def handle_event(self, event):
        transactions = self.transaction_repository

        self.logger.debug('Received transaction event', received_event=event)

        account_number = event['accountNumber']
        amount = int(event['amount'])

        if not self._account_exists(account_number):
            self.logger.warning(
                'Attempted transaction against inactive '
                'account',
                account_number=account_number,
                amount=amount)
            return

        transactions.store({'accountNumber': account_number,
                            'amount': amount})

        transactions = transactions.fetch_by_account_number(account_number)

        balance = sum([tx['amount'] for tx in transactions])

        self.balance_updates.produce(
            json.dumps({'accountNumber': account_number,
                        'balance': balance}))

        self.logger.info('Successful transaction',
                         account_number=account_number,
                         amount=amount,
                         balance=balance)

    def _account_exists(self, account_number):
        return self.accounts_client.has_active_account(account_number)
