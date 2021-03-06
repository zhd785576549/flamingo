from importlib import import_module
import json
import re
from urllib import parse
from flamingo.utils import exc
from flamingo.utils import parser


def import_module_string(mod_str: str):
    """
    Import module string
    :param mod_str: [str] Module path
    :return: Module
    """
    mod = import_module(mod_str)
    return mod


def load_class(mod_cls_str):
    """
    加载指定路径的类
    :param mod_cls_str: [str] 类路径
    :return:
    """
    try:
        mod_path, cls_name = mod_cls_str.split(":")
        mod = import_module_string(mod_path)
        if hasattr(mod, cls_name):
            cls = getattr(mod, cls_name)
            return cls
        else:
            raise exc.ClassNotFoundError(f"Class path not found named {mod_cls_str}")
    except IndexError:
        raise exc.ClassNotFoundError(f"Class path not found named {mod_cls_str}")
    except ImportError:
        raise exc.ClassNotFoundError(f"Class path not found named {mod_cls_str}")


def safe_json_loads(data):
    """
    安全json反序列化
    :param data: 字符串
    :return:
    """
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None


async def read_body(receive):
    """
    获取传递过来的请求body数据
    """
    body = b''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body


async def trans_body_data(receiver, headers, decoding="UTF-8"):
    """
    将请求的数据转换成字典数据
    :param receiver: 数据流
    :param headers: 请求头数据
    :param decoding: 解码方式
    :return:
    """
    if receiver:
        return await parser.FormParser(headers=headers, charset=decoding, receiver=receiver).parse()
    else:
        return None


def trans_params_to_dict(scope_ins, decoding="UTF-8"):
    """
    将字节的query_string转换成字典类型
    :param scope_ins: 字节原始参数
    :param decoding: 编码格式
    :return:
    """
    return parser.ParseQueryParser(scope=scope_ins, charset=decoding).parse()


def get_url_name(view_func, name):
    """
    获取视图方法名称

    :param view_func: 视图方法
    :param name: 自定义名称
    :return:
    """
    if name and isinstance(name, str):
        return name
    elif callable(view_func):
        return view_func.__name__
    else:
        return None


def url_prefix_join(path: str, prefix: str):
    """
    路由添加前缀
    :param path: 原始路由
    :param prefix: 前缀
    :return:
    """
    _url1 = prefix.rstrip("/")
    _url2 = path.lstrip("/")
    return f"{_url1}/{_url2}"


def url_join(path: str, *path_list):
    """
    连接多个的路径
    :param path: 原始path路径
    :param path_list: 需要连接的路径列表
    :return:
    """
    if path.endswith("/"):
        path = path.rstrip("/")
    for arg in path_list:
        if arg.startswith("/"):
            arg = arg.lstrip("/")
        path = f"{path}/{arg}"
    return path


def trans_headers(headers):
    """
    将原有的headers转化为标准的字典格式
    :param headers: scope中的headers信息
    :return:
    """
    headers = {
        k.decode("UTF-8"): v.decode("UTF-8")
        for k, v in headers
    }
    return headers
