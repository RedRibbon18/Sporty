import requests
import logging
from framework.config import get_environment_config

logger = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, base_url: str | None = None, env: str | None = None):
        config = get_environment_config(env)
        self.base_url = (base_url or config.api_base_url).rstrip("/")
        self.session = requests.Session()

    def _generate_url(self, endpoint):
        return self.base_url + "/" + endpoint

    def get(self, endpoint: str, params=None, headers=None):
        url = self._generate_url(endpoint)
        logger.info(f"GET request to {url},\nwith params:{params}\nheaders:{headers}")
        return self.session.get(
            url,
            params=params,
            headers=headers
        )

    def post(self, endpoint: str, json=None, data=None, headers=None):
        url = self._generate_url(endpoint)
        logger.info(f"POST request to {url},\nwith json:{json}\ndata: {data}\nheaders:{headers}")
        return self.session.post(
            url,
            json=json,
            data=data,
            headers=headers,
        )

    def put(self, endpoint: str, json=None, data=None, headers=None):
        url = self._generate_url(endpoint)
        logger.info(f"PUT request to {url},\nwith json:{json}\ndata: {data}\nheaders:{headers}")
        return self.session.put(
            url,
            json=json,
            data=data,
            headers=headers,
        )

    def delete(self, endpoint: str, params=None, headers=None):
        url = self._generate_url(endpoint)
        logger.info(f"DELETE request to {url},\nwith params:{params}\nheaders:{headers}")
        return self.session.delete(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            params=params,
            headers=headers
        )
