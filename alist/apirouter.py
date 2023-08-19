import inspect
import json
import sys
import warnings

from alist.connection import Connection
from alist.info import FileInfo, SettingInfo, UserInfo, StorageInfo, Driver, WebdavPolicy, ExtractFolder


class Router:

    def __init__(self, father: "Router", connection: Connection):
        self._father = father
        self._api_path = "" if self._father is None else self._father._api_path
        self._connection = connection


class APIRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/api"

        self.admin = AdminRouter(self, self._connection)
        self.fs = FsRouter(self, connection=self._connection)
        self.auth = AuthRouter(self, connection=self._connection)

    def __str__(self):
        self.router_path = "/api"


class AdminRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/admin"

        self.meta = MetaRouter(self, self._connection)
        self.user = UserRouter(self, self._connection)
        self.storage = StorageRouter(self, self._connection)
        self.driver = DriverRouter(self, self._connection)
        self.setting = SettingRouter(self, self._connection)
        self.task = TaskRouter(self, self._connection)


class AuthRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/auth"

    def login(self, username, password, otp_code=""):
        payload = {"username": username,
                   "password": password,
                   "otp_code": ""}
        rsp = self._connection.request("post", f"{self._api_path}/{inspect.stack()[0].function}",
                                       data=json.dumps(payload))
        self._connection.set_token(rsp.json()["data"]["token"])


class FsRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/fs"

    def list(self, path: str, password="", page=1, per_page=30, refresh=False):
        payload = {
            "page": page,
            "password": password,
            "path": path,
            "per_page": per_page,
            "refresh": refresh
        }
        rsp = self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}",
                                       data=json.dumps(payload))
        ret = []
        for info in rsp.json()["data"]["content"]:
            ret.append(FileInfo(info))
        return ret

    def mkdir(self, path: str):
        payload = {
            "path": path
        }
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}",
                                 data=json.dumps(payload))

    def rename(self, name: str, path: str):
        payload = {
            "name": name,
            "path": path
        }
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}",
                                 data=json.dumps(payload))

    def remove(self, from_dir: str, names: [str]):
        payload = {
            "dir": from_dir,
            "names": names
        }
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}",
                                 data=json.dumps(payload))

    def get(self, path: str, password: str = ""):
        payload = {
            "path": path,
            "password": password
        }
        rsp = self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}",
                                       data=json.dumps(payload))
        return FileInfo(rsp.json()["data"])


class MetaRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/meta"


class UserRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/user"

    def list(self):
        rsp = self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")
        ret = []
        for i in rsp.json()["data"]["content"]:
            ret.append(UserInfo(i))
        return ret


class StorageRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/storage"

    def list(self):
        rsp = self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")
        ret = []
        for i in rsp.json()["data"]["content"]:
            ret.append(StorageInfo(i))
        return ret

    def get(self, storage_id):
        payload = {
            "id": storage_id
        }
        rsp = self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}", params=payload)
        return StorageInfo(rsp.json()["data"])

    def create(self, mount_path, order: int, driver: Driver,
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
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}", data=json.dumps(payload))

    def delete(self, storage_id):
        payload = {
            "id": storage_id
        }
        self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}", params=payload)


class DriverRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/driver"

    def list(self):
        """不要用，看看就好了"""
        rsp = self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")
        warnings.warn("打印出来你自己看吧")
        print(rsp.json())


class SettingRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/setting"

    def list(self, group=0):
        payload = {
            "group": group
        }
        rsp = self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}",
                                       params=payload)
        ret = []
        for i in rsp.json()["data"]:
            ret.append(SettingInfo(i))
        return ret


class TaskRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/task"
