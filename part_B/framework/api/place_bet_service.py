from framework.api.api_client import ApiClient
from framework.api import endpoints

class PlaceBetService(ApiClient):

    def place_bet(self, json, headers):
        return self.post(endpoints.PLACE_BET, json=json, headers=headers)