import json
from strenum import StrEnum

import dateutil.parser


class WebdavPolicy(StrEnum):
    """我只知道这一个"""
    R302 = "302_redirect"


class ExtractFolder(StrEnum):
    """
    提取文件夹方法
    """
    Front = "front"
    End = "end"


class Driver(StrEnum):
    """
    其他的还没找出来
    """
    Local = "Local"
    Aliyundrive = "Aliyundrive"


def _get_value(json_dict: dict, key, default=None):
    if key == "modified":
        modified_str = json_dict.get(key, "1970-01-01T00:00:00:000Z")
        # go time is diff
        v = dateutil.parser.parser().parse(modified_str)
    elif key == "addition":
        v = json.loads(json_dict.get(key, "{}"))
    else:
        v = json_dict.get(key, None)
    return v


class Info:
    _default = {}

    def __init__(self):
        pass

    @classmethod
    def creatInfo(cls, info_cls: type, info_json):
        return info_cls(info_json)

    @classmethod
    def retInfo(cls, info_cls: type, info_json):
        if isinstance(info_json, dict):
            return info_cls(info_json)
        if isinstance(info_json, list):
            return [info_cls(i) for i in info_json]

    def trans(self, info_json: dict):
        for k in self._default:
            v = info_json.get(k, None)

            self.__setattr__(k, v)


class FileInfo(Info):
    _default = {
        "name": "name",
        "size": 1,
        "is_dir": False,
        "modified": "1970-01-01T00:00:00:000Z",
        "sign": "xxxx",
        "thumb": "",
        "type": 5,
        "raw_url": "",
        "readme": "",
        "provider": "Aliyundrive",
        "related": None
    }

    def __init__(self, info_json):
        super().__init__()
        # 这里是为了自动补全加的，不然很不好用
        self.name = None
        self.size = None
        self.is_dir = None
        self.sign = None
        self.thumb = None
        self.type = None
        self.modified = None
        self.raw_url = None
        self.readme = None
        self.provider = None
        self.related = None

        self.trans(info_json)

    def __str__(self):
        return f"{self.__class__}[name:{self.name},size:{self.size},is_dir:{self.is_dir},modified:{self.modified}]"


class SettingInfo(Info):
    _default = {
        "key": "version",
        "value": "v3.5.1",
        "help": "",
        "type": "string",
        "options": "",
        "group": 0,
        "flag": 2
    }

    def __init__(self, info_json):
        super().__init__()
        # 这里是为了自动补全加的，不然很不好用
        self.key = None
        self.value = None
        self.type = None
        self.options = None
        self.group = None
        self.flag = None

        self.trans(info_json)

    def __str__(self):
        return f"{self.__class__}[key:{self.key},value:{self.value}]"


class UserInfo(Info):
    _default = {
        "id": 1,
        "username": "admin",
        "password": "",
        "base_path": "/",
        "role": 2,
        "permission": 0
    }

    def __init__(self, info_json):
        super().__init__()
        # 这里是为了自动补全加的，不然很不好用
        self.id = None
        self.username = None
        self.password = None
        self.base_path = None
        self.role = None
        self.permission = None
        self.trans(info_json)

    def __str__(self):
        return f"{self.__class__}[username:{self.username},base_path:{self.base_path}]"


class StorageInfo(Info):
    _default = {
        "id": 1,
        "mount_path": "/阿里云盘",
        "order": 0,
        "driver": "Aliyundrive",
        "cache_expiration": 30,
        "status": "work",
        "addition": "{\"root_folder_id\":\"xxx\",\"refresh_token\":\"xxx\",\"order_by\":\"name\","
                    "\"order_direction\":\"ASC\",\"rapid_upload\":false}",
        "remark": "",
        "modified": "2022-11-26T18:55:55.261579727+08:00",
        "disabled": False,
        "order_by": "",
        "order_direction": "",
        "extract_folder": "",
        "web_proxy": False,
        "webdav_policy": "302_redirect",
        "down_proxy_url": ""
    }

    def __init__(self, info_json):
        super().__init__()
        # 这里是为了自动补全加的，不然很不好用
        self.id = None
        self.mount_path = None
        self.order = None
        self.driver = None
        self.cache_expiration = None
        self.status = None
        self.addition = None
        self.modified = None
        self.disabled = None
        self.order_by = None
        self.order_direction = None
        self.extract_folder = None
        self.web_proxy = None
        self.webdav_policy = None
        self.down_proxy_url = None

        self.trans(info_json)

    def __str__(self):
        return f"{self.__class__}[driver:{self.driver},mount_path:{self.mount_path},modified:{self.modified}]"


class MetaInfo(Info):
    _default = {
        "id": 1,
        "path": "/a",
        "password": "i",
        "p_sub": False,
        "write": False,
        "w_sub": False,
        "hide": "",
        "h_sub": False,
        "readme": "",
        "r_sub": False
    }

    def __init__(self, info_json):
        super().__init__()
        # 这里是为了自动补全加的，不然很不好用
        self.id = None
        self.path = None
        self.password = None
        self.p_sub = None
        self.write = None
        self.w_sub = None
        self.hide = None
        self.h_sub = None
        self.readme = None
        self.r_sub = None

        self.trans(info_json)

    def __str__(self):
        return f"{self.__class__}[path:{self.path},password:{self.password}]"


class TaskInfo(Info):
    _default = {
        "id": "1",
        "name": "upload 1.png to [/s](/test)",
        "state": "succeeded",
        "status": "",
        "progress": 100,
        "error": ""
    }

    def __init__(self, info_json):
        super().__init__()
        # 这里是为了自动补全加的，不然很不好用
        self.id = None
        self.name = None
        self.state = None
        self.status = None
        self.progress = None
        self.error = None

        self.trans(info_json)

    def __str__(self):
        return f"{self.__class__}[path:{self.name},password:{self.state}]"
