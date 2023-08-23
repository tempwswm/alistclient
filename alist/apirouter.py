import abc
import inspect
import json
import sys
import warnings

from alist.connection import Connection
from alist.info import FileInfo, SettingInfo, UserInfo, StorageInfo, Driver, WebdavPolicy, ExtractFolder, TaskInfo, Info


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
        self.public = PublicRouter(self, connection=self._connection)

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
        self.message = MessageRouter(self, self._connection)
        self.index = IndexRouter(self, self._connection)


class AuthRouter(Router):
    """这里有一些url和函数名不能对应了。。。。。"""

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

    def login_hash(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/login/hash")

    def generate_2fa(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/2fa/generate")

    def verify_2fa(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/2fa/verify")


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

        return Info.retInfo(FileInfo, rsp.json()["data"]["content"])

    def search(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def get(self, path: str, password: str = ""):
        payload = {
            "path": path,
            "password": password
        }
        rsp = self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}",
                                       data=json.dumps(payload))
        return FileInfo(rsp.json()["data"])

    def other(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def dirs(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

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

    def batch_rename(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def regex_rename(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def move(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def recursive_move(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def copy(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def remove(self, from_dir: str, names: [str]):
        payload = {
            "dir": from_dir,
            "names": names
        }
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}",
                                 data=json.dumps(payload))

    def remove_empty_directory(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def put(self):
        # TODO
        self._connection.request("PUT", f"{self._api_path}/{inspect.stack()[0].function}")

    def form(self):
        # TODO
        self._connection.request("PUT", f"{self._api_path}/{inspect.stack()[0].function}")

    def link(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def add_arai2(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def add_qbit(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")


class PublicRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/public"

    def ping(self):
        # TODO
        self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")

    def setting(self):
        # TODO
        self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")


class MetaRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/meta"

    def list(self):
        # TODO
        self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")

    def get(self):
        # TODO
        self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")

    def create(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def update(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def delete(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")


class UserRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/user"

    def list(self):
        rsp = self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")
        return Info.retInfo(UserInfo, rsp.json()["data"]["content"])

    def get(self):
        # TODO
        self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")

    def create(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def update(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def cancel_2fa(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def del_cache(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")


class StorageRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/storage"

    def list(self):
        rsp = self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")
        return Info.retInfo(StorageInfo, rsp.json()["data"]["content"])

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

    def update(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def delete(self, storage_id):
        payload = {
            "id": storage_id
        }
        self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}", params=payload)

    def enable(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def disable(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def load_all(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")


class DriverRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/driver"

    def list(self):
        """不要用，看看就好了"""
        rsp = self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")
        warnings.warn("打印出来你自己看吧")
        print(rsp.json())

    def names(self):
        # TODO
        self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")

    def info(self):
        # TODO
        self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")


class SettingRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/setting"

    def get(self):
        # TODO
        self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")

    def list(self, group=0):
        payload = {
            "group": group
        }
        rsp = self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}",
                                       params=payload)
        return Info.retInfo(SettingInfo, rsp.json()["data"]["content"])

    def save(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def delete(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def reset_token(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def set_aria2(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def set_qbit(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")


class TaskRouter(Router):
    """
    任务
    """

    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/task"

        self.upload = TaskUploadRouter(self, self._connection)
        self.copy = TaskCopyRouter(self, self._connection)
        self.aria2_down = TaskAria2DownRouter(self, self._connection)
        self.aria2_transfer = TaskAria2TransferRouter(self, self._connection)
        self.qbit_down = TaskQbitDownRouter(self, self._connection)
        self.qbit_transfer = TaskQbitTransferRouter(self, self._connection)


class MessageRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/message"

    def get(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def send(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")


class IndexRouter(Router):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/index"

    def build(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def update(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def stop(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def clear(self):
        # TODO
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def progress(self):
        # TODO
        self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")


class _TaskBaseRouter(Router):
    """
    是task类型api的接口定义类
    """

    @abc.abstractmethod
    def __init__(self, father, connection):
        super().__init__(father, connection)

    def done(self):
        rsp = self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")
        return Info.retInfo(TaskInfo, rsp.json()["data"]["content"])

    def undone(self):
        rsp = self._connection.request("GET", f"{self._api_path}/{inspect.stack()[0].function}")
        return Info.retInfo(TaskInfo, rsp.json()["data"]["content"])

    def delete(self, tid):
        payload = {"tid": tid}
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}", params=payload)

    def cancel(self, tid):
        payload = {"tid": tid}
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}", params=payload)

    def clear_done(self):
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def clear_succeeded(self):
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}")

    def retry(self, tid):
        payload = {"tid": tid}
        self._connection.request("POST", f"{self._api_path}/{inspect.stack()[0].function}", params=payload)


class TaskUploadRouter(_TaskBaseRouter):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/upload"


class TaskCopyRouter(_TaskBaseRouter):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/copy"


class TaskAria2DownRouter(_TaskBaseRouter):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/aria2_down"


class TaskAria2TransferRouter(_TaskBaseRouter):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/aria2_transfer"


class TaskQbitDownRouter(_TaskBaseRouter):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/qbit_down"


class TaskQbitTransferRouter(_TaskBaseRouter):
    def __init__(self, father, connection):
        super().__init__(father, connection)
        self._api_path += "/qbit_down"
