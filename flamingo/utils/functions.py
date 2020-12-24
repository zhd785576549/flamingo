from importlib import import_module
import json
from flamingo.utils import exc


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


def trans_str_to_dict(b_data, decoding="UTF-8"):
    if b_data:
        return safe_json_loads(data=b_data.decode(decoding))
    else:
        return None


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

