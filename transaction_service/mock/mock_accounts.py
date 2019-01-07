class MockAccounts:
    def __init__(self):
        self._accounts = set()

    def add(self, account_number):
        self._accounts.add(account_number)

    def has_account_with_number(self, account_number):
        return account_number in self._accounts
