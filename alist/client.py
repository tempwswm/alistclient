from alist.apirouter import APIRouter
from alist.connection import Connection
from alist.info import StorageInfo, WebdavPolicy, ExtractFolder, Driver


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
        """你可以用它来自己实现一些这个库没有的东西"""
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

    def upload(self, file, remote_path):
        raise Exception("这里还没实现")
        # return self.api.fs.put()

    def upload_files(self, files: list, remote_path):
        raise Exception("这里还没实现")
        # return self.api.fs.form()

    def get(self, path: str, password: str = ""):
        return self.api.fs.get(path, password)

    def put(self):
        return self.upload(None, None)

    def list_setting(self, group=0):
        return self.api.admin.setting.list(group)

    def list_user(self):
        return self.api.admin.user.list()

    def list_storage(self):
        return self.api.admin.storage.list()

    def enable_storage(self, storage_id):
        return self.api.admin.storage.enable(storage_id)

    def disable_storage(self, storage_id):
        return self.api.admin.storage.disable(storage_id)

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

    def __init__(self, domain, username, password, webhook_url):
        super().__init__(domain, username, password)
        self._register_webhook(webhook_url)

    def _register_webhook(self, webhook_url):
        pass
