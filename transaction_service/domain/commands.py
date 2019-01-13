import json


class CreditAccount:
    def __init__(self,
                 transaction_repository,
                 balance_updates,
                 accounts_client,
                 logger):
        self.transaction_repository = transaction_repository
        self.balance_updates = balance_updates
        self.accounts_client = accounts_client
        self.logger = logger

    def execute(self, account_number, amount):
        if not self._account_exists(account_number):
            self.logger.warning(
                'Attempted transaction against inactive account',
                account_number=account_number,
                amount=amount)
            return

        transaction = dict(accountNumber=account_number, amount=amount)
        self.transaction_repository.store(transaction)

        balance = self._get_account_balance(account_number)

        self._produce_update(account_number, balance)

        self.logger.info('Successful transaction',
                         account_number=account_number,
                         amount=amount,
                         balance=balance)

    def _produce_update(self, account_number, balance):
        balance_update = json.dumps(dict(accountNumber=account_number,
                                         balance=balance))
        self.balance_updates.produce(balance_update)

    def _get_account_balance(self, account_number):
        transactions = self.fetch_transactions(account_number)
        return sum([tx['amount'] for tx in transactions])

    def fetch_transactions(self, account_number):
        return self.transaction_repository \
            .fetch_by_account_number(account_number)

    def _account_exists(self, account_number):
        return self.accounts_client.has_active_account(account_number)
