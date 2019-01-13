from schema import Schema, And, SchemaError

from transaction_service.domain.commands import CreditAccount

TRANSACTION_SCHEMA = Schema(dict(
    id=And(str, len),
    accountNumber=And(str, lambda s: len(s) == 8),
    amount=And(int, lambda n: n > 0),
    operation=And(str, lambda s: s in ['credit', 'debit']),
    status='accepted',
    created=And(str, len)))


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
        self.logger.debug('Received transaction event', received_event=event)

        if not self._schema_is_valid(event):
            return

        account_number = event['accountNumber']
        amount = int(event['amount'])

        self._credit_account_command().execute(account_number, amount)

    def _credit_account_command(self):
        return CreditAccount(
            transaction_repository=self.transaction_repository,
            balance_updates=self.balance_updates,
            accounts_client=self.accounts_client,
            logger=self.logger)

    def _schema_is_valid(self, event):
        try:
            TRANSACTION_SCHEMA.validate(event)
            return True
        except SchemaError as e:
            self.logger.warning('Invalid transaction event',
                                error=str(e),
                                received_event=event)
            return False
