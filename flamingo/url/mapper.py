from werkzeug import routing
from bidict import bidict
from flamingo.url import conf
from flamingo.utils import functions
from flamingo.utils import exc


def get_routers(url_mod_str, target="routers"):
    url_mod = functions.import_module_string(url_mod_str)
    if hasattr(url_mod, target):
        return getattr(url_mod, target)
    else:
        raise exc.ConfigureError(f"Module url_mod_str cannot find {target}.")


class RouterMapper:

    def __init__(self):
        self.__mapper = routing.Map()
        self.__endpoint_mapper = bidict()

    @property
    def mapper(self):
        return self.__mapper

    def match_url(self):
        return self.__mapper

    def add_rule(self, rule, **options):
        self.__mapper.add(rule)

    def load_url_from_conf(self, url_conf: str):
        """
        加载所有路由
        :param url_conf: [str] 配置文件中的顶级路由配置
        :return:
        """
        routers = get_routers(url_mod_str=url_conf)
        for path in routers:
            self.__load_urls(path)

    def __load_urls(self, path, prefix_path=None):
        """
        加载路由
        :param path: path对象或者下级路由
        :param prefix_path: 如果是从下级路由过来，那么前缀是上级的路由
        :return:
        """
        if isinstance(path.view_func_or_module, str):
            # 如果是下级路由
            routers = get_routers(url_mod_str=path.view_func_or_module)
            if prefix_path is None:
                prefix_path = path.url
            else:
                prefix_path = functions.url_prefix_join(path=path.url, prefix=prefix_path)
            for _path in routers:
                self.__load_urls(path=_path, prefix_path=prefix_path)
        elif callable(path.view_func_or_module):
            if prefix_path:
                path.url = functions.url_prefix_join(path=path.url, prefix=prefix_path)
            rule = routing.Rule(
                string=path.url,
                endpoint=path.name
            )
            self.add_rule(rule)
            self.__endpoint_mapper[path.name] = path.view_func_or_module

    def get_view_func(self, name):
        """
        获取视图方法
        :param name: 视图名称
        :return:
        """
        return self.__endpoint_mapper.get(name)
