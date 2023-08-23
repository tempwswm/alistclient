import json
import warnings

import requests

from alist.apirouter import APIRouter
from alist.connection import Connection
from alist.info import FileInfo, UserInfo, StorageInfo, SettingInfo, WebdavPolicy, ExtractFolder, Driver


class Client:

    def __init__(self, domain, username, password):
        self.domain = domain
        self.connection = Connection(domain)
        self.token = None
        self.username = username
        self.password = password
        self.api = APIRouter(None, self.connection)

        # self.login()

    @property
    def hash_password(self):
        return None
        # TODO 给hash_login用的混淆后的密码，没看懂怎么实现的

    def request(self, method="POST", url="", params=None, data=None):
        return self.connection.request(method, url, params, data)

    def login(self):
        return self.api.auth.login(self.username, self.password)

    def list(self, path: str, password="", page=1, per_page=30, refresh=False):
        return self.api.fs.list(path, password, page, per_page, refresh)

    def mkdir(self, path: str):
        return self.api.fs.mkdir(path)

    def rename(self, name: str, path: str):
        return self.api.fs.rename(name, path)

    def remove(self, from_dir: str, names: [str]):
        return self.api.fs.remove(from_dir, names)

    def upload(self):
        # TODO
        # /api/fs/form
        # 我没找到怎么实现的，如果你能提供curl命令，我会补全
        pass

    def get(self, path: str, password: str = ""):
        return self.api.fs.get(path, password)

    def put(self):
        # TODO
        # /api/fs/put
        # 我没找到怎么实现的，如果你能提供curl命令，我会补全
        pass

    def list_setting(self, group=0):
        return self.api.admin.setting.list(group)

    def list_user(self):
        return self.api.admin.user.list()

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
        return self.api.admin.storage.create(mount_path, order, driver,
                                             remark, cache_expiration,
                                             web_proxy, webdav_policy,
                                             down_proxy_url, extract_folder,
                                             addition)

    def get_storage(self, storage_id):
        return self.api.admin.storage.get(storage_id)

    def delete_storage(self, storage_id):
        return self.api.admin.storage.delete(storage_id)

    def list_driver(self):
        return self.api.admin.driver.list()


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
