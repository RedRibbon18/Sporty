from framework.api.api_client import ApiClient
from framework.api import endpoints


class MatchService(ApiClient):

    def get_matches(self, headers):
        return self.get(endpoints.MATCHES, headers=headers)