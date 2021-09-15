from dataclasses import dataclass

import requests


@dataclass
class BearerAuth(requests.auth.AuthBase):
    token: str

    def __call__(self, request):
        request.headers['authorization'] = f'Bearer {self.token}'
        return request
