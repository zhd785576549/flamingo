class Path:
    """
    路径信息类

    :param url 请求路由
    :param name 请求方法别名，默认是请求方法的名称 xxx.__name__
    :param view_func_or_module 请求方法或者下级路由模块
    """

    def __init__(self, url=None, name=None, view_func_or_module=None):
        self.__url = url
        self.__name = view_func_or_module.__name__ if view_func_or_module and callable(view_func_or_module) else name
        self.__view_or_mod = view_func_or_module

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def name(self):
        return self.__name

    @property
    def view_func_or_module(self):
        return self.__view_or_mod


def path(url=None, view_func_or_module=None, name=None):
    """
    路径构造器

    :param url: 请求路由
    :param name: 请求方法别名，默认是请求方法的名称 xxx.__name__
    :param prefix: 前缀名称
    :param suffix: 后缀名称
    :param view_func_or_module: 请求方法或者下级路由模块路径
    :return:
    """
    return Path(
        url=url,
        view_func_or_module=view_func_or_module,
        name=name
    )
