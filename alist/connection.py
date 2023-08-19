import inspect
import warnings

import requests


class Connection:
    def __init__(self, domain):
        self.domain = domain
        self.session = requests.Session()
        self.token = ""

    def request(self, method="POST", url="", params=None, data=None):

        # caller = inspect.stack()
        # url = f"{caller[1].frame.f_locals['self']._api_path}/{caller[1].function}"
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        rsp = self.session.request(method=method, url=self.domain + url, headers=headers, params=params, data=data)
        if rsp.status_code != 200:
            raise Exception("not 200, check")
        rsp_json = rsp.json()
        if rsp_json["code"] != 200:
            warnings.warn(rsp_json["message"])
        return rsp

    def set_token(self, token):
        self.token = token

    def get(self, url="", params=None, data=None):
        self.request("GET", url, params, data)

    def post(self, url="", params=None, data=None):
        self.request("Post", url, params, data)
