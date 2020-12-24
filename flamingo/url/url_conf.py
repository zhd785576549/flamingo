import bidict
from flamingo.utils import functions
import sys


class Url:

    def __init__(self, path, view_func, prefix=None, name=None, func_alias=None, url_pattern=None):
        self.__path = path
        self.__view_func = view_func
        self.__prefix = prefix
        self.__name = name
        self.__func_alias = func_alias
        self.__url_pattern = url_pattern

    @property
    def path(self):
        return self.__path

    @property
    def view_func(self):
        return self.__view_func

    @property
    def prefix(self):
        return self.__prefix

    @property
    def name(self):
        return self.__name

    @path.setter
    def path(self, path):
        self.__path = path

    @property
    def func_alias(self):
        return self.__func_alias

    @property
    def url_pattern(self):
        return self.__url_pattern


def url(path, view_func=None, prefix=None, name=None, func_alias=None):
    return Url(path=path, view_func=view_func, prefix=prefix, name=name, func_alias=func_alias)


class UrlMapper:
    """
    __url_mapper

    正字典
    {
        "url_path": "name"
    }

    反向字典
    {
        "name": "url_path"
    }

    __name_mapper
    正向字典

    {
        "name": view_func
    }

    反向字典

    {
        view_func: "name"
    }
    """

    def __init__(self):
        self.__url_mapper = bidict.bidict()
        self.__name_mapper = bidict.bidict()

    def build_url_mapper(self, url_module_path=None):
        """
        生成路由表
        :param url_module_path: 路由模块路径
        :return:
        """
        url_module = functions.import_module_string(url_module_path)
        identify_name = "routers"
        if hasattr(url_module, identify_name):
            routers = getattr(url_module, identify_name)
            for router in routers:
                if isinstance(router, Url):
                    self.add_router(_url=router)

    def add_router(self, _url: Url):
        """
        添加路由到mapper中，并且将视图方法对应到name_mapper中

        :param _url: Url路径
        :return:
        """
        if _url.prefix:
            _url.path = functions.url_prefix_join(_url.prefix, _url.path)

        if _url.view_func is None:
            return
        elif callable(_url.view_func):
            # 如果是可执行的方法，那么将记录方法名称和方法本身以及路由的对应关系，双向的对应
            # 这里如果已经绑定了还需要绑定另外一个地址，可以使用func_alias参数进行指定
            func_name = _url.func_alias or _url.view_func.__name__
            self.__url_mapper.put(_url.path, func_name)
            self.__name_mapper.put(func_name, _url.view_func)
        elif isinstance(_url.view_func, str):
            url_module = functions.import_module_string(_url.view_func)
            if hasattr(url_module, "routers"):
                routers = getattr(url_module, "routers")
                for router in routers:
                    if isinstance(router, Url):
                        if _url.name:
                            # 如果是模块并且定义了name名称，默认取的view_func的名称，那么每个path的后缀就是这个name名称
                            router.path = functions.url_join(_url.path, router.path)
                            self.add_router(_url=router)

    def get_mapper(self):
        """
        获取路由表
        :return:
        """
        return self.__url_mapper

    def get_func_name(self, path):
        """
        获取路由表中的方法名称
        :param path:
        :return:
        """
        return self.__url_mapper.get(path)

    def get_url_path(self, func_name):
        """
        获取方法名称对应的路由
        :param func_name:
        :return:
        """
        return self.__url_mapper.inverse.get(func_name)

    def get_view_func(self, func_name):
        """
        获取视图方法
        :param func_name: 方法名称
        :return:
        """
        return self.__name_mapper.get(func_name)

    def display_url_mapper(self):
        """
        输出所有路由列表
        :return:
        """
        sys.stdout.write("\n\rAvailable urls:")
        for k in self.__url_mapper.keys():
            sys.stdout.write(f"\n\r{k}")
        sys.stdout.write("\n\r")

    def get_url_mapper(self):
        """
        获取路由表
        :return:
        """
        return self.__url_mapper.items()

    def get_url_pattern(self, func_name):
        """
        返回路由匹配规则
        :return:
        """
        _url = self.__name_mapper.get(func_name)
        if isinstance(_url, Url):
            return _url.url_pattern
        else:
            return None
