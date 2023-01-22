from requests import Response
from requests import request
from urllib.parse import urljoin

class HTTPClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def request(self, method: str, url: str, **kwargs) -> Response:
        full_url = urljoin(self.base_url, url)
        response = request(method, full_url, **kwargs)
        response.raise_for_status()
        return response
