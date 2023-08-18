import json
import warnings

import requests

from alist.info import FileInfo, UserInfo, StorageInfo, SettingInfo, WebdavPolicy, ExtractFolder, Driver


class Client:

    def __init__(self, domain, username, password):
        self.domain = domain
        self.session = requests.Session()
        self.token = None
        self.username = username
        self.password = password

        # self.login()

    @property
    def hash_password(self):
        return None
        # TODO ???????

    def request(self, method="POST", url="", params=None, data=None):
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

    def login(self):

        payload = {"username": self.username,
                   "password": self.password,
                   "otp_code": ""}
        rsp = self.request("post", "/api/auth/login", data=json.dumps(payload))
        self.token = rsp.json()["data"]["token"]

    def list(self, path: str, password="", page=1, per_page=30, refresh=False):
        payload = {
            "page": page,
            "password": password,
            "path": path,
            "per_page": per_page,
            "refresh": refresh
        }
        rsp = self.request("POST", "/api/fs/list", data=json.dumps(payload))
        ret = []
        for info in rsp.json()["data"]["content"]:
            ret.append(FileInfo(info))
        return ret

    def mkdir(self, path: str):
        payload = {
            "path": path
        }
        self.request("POST", "/api/fs/mkdir", data=json.dumps(payload))

    def rename(self, name: str, path: str):
        payload = {
            "name": name,
            "path": path
        }
        self.request("POST", "/api/fs/rename", data=json.dumps(payload))

    def remove(self, from_dir: str, names: [str]):
        payload = {
            "dir": from_dir,
            "names": names
        }
        self.request("POST", "/api/fs/remove", data=json.dumps(payload))

    def upload(self):
        # TODO
        # /api/fs/form
        # 我没找到怎么实现的，如果你能提供curl命令，我会补全
        pass

    def get(self, path: str, password: str = ""):
        payload = {
            "path": path,
            "password": password
        }
        rsp = self.request("POST", "/api/fs/get", data=json.dumps(payload))
        return FileInfo(rsp.json()["data"])

    def put(self):
        # TODO
        # /api/fs/put
        # 我没找到怎么实现的，如果你能提供curl命令，我会补全
        pass

    def list_setting(self, group=0):
        payload = {
            "group": group
        }
        rsp = self.request("GET", "/api/admin/setting/list", params=payload)
        ret = []
        for i in rsp.json()["data"]:
            ret.append(SettingInfo(i))
        return ret

    def list_user(self):

        rsp = self.request("GET", "/api/admin/user/list")
        ret = []
        for i in rsp.json()["data"]["content"]:
            ret.append(UserInfo(i))
        return ret

    def list_storage(self):
        rsp = self.request("GET", "/api/admin/storage/list")
        ret = []
        for i in rsp.json()["data"]["content"]:
            ret.append(StorageInfo(i))
        return ret

    def enable_storage(self, storage_id):
        payload = {
            "id": storage_id
        }
        self.request("POST", "/api/admin/storage/enable", params=payload)

    def disable_storage(self, storage_id):
        payload = {
            "id": storage_id
        }
        self.request("POST", "/api/admin/storage/disable", params=payload)

    def create_storage(self, mount_path, order: int, driver: Driver,
                       remark: str = None, cache_expiration: int = 30,
                       web_proxy: bool = False, webdav_policy: WebdavPolicy = WebdavPolicy.R302,
                       down_proxy_url: str = "", extract_folder: ExtractFolder = ExtractFolder.Front,
                       addition=None):
        """不一定能用"""
        #
        if addition is None:
            addition = {}
        payload = {
            "mount_path": mount_path,
            "order": order,
            "remark": remark,
            "cache_expiration": cache_expiration,
            "web_proxy": web_proxy,
            "webdav_policy": webdav_policy,
            "down_proxy_url": down_proxy_url,
            "extract_folder": extract_folder,
            "driver": driver,
            "addition": addition
        }
        self.request("POST", "/api/admin/storage/create", data=json.dumps(payload))

    def get_storage(self, storage_id):
        payload = {
            "id": storage_id
        }
        rsp = self.request("GET", "/api/admin/storage/get", params=payload)
        return StorageInfo(rsp.json()["data"])

    def delete_storage(self, storage_id):
        payload = {
            "id": storage_id
        }
        self.request("GET", "/api/admin/storage/delete", params=payload)

    def list_driver(self):
        """不要用，看看就好了"""
        rsp = self.request("GET", "/api/admin/driver/list")
        warnings.warn("打印出来你自己看吧")
        print(rsp.json())


class WebHookClient(Client):
    """
    这是一个处理webhook的客户端
    与https://github.com/alist-org/alist/issues/5032要求的一致，先放这里，以后实现
    """
    def __init__(self, domain, webhook_url):
        super().__init__(domain)
        self._register_webhook(webhook_url)

    def _register_webhook(self, webhook_url):
        pass
