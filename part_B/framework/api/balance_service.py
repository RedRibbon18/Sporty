from framework.api.api_client import ApiClient
from framework.api import endpoints

class BalanceService(ApiClient):

    def get_balance(self, headers):
        return self.get(endpoints.BALANCE, headers=headers)