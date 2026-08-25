from framework.api.api_client import ApiClient
from framework.api import endpoints

class ResetBalanceService(ApiClient):

    def reset_balance(self, headers):
        return self.post(endpoints.RESET_BALANCE, headers=headers)