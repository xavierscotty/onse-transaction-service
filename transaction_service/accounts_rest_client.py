import requests

class AccountsRestClient:
    def __init__(self, url):
        self.url = url

    def has_account_with_number(self, account_number):
        url = f'{self.url}/accounts/{account_number}'

        response = requests.get(url)

        if response.status_code is 200:
            return True
        else:
            return False
