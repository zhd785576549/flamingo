from flamingo.utils import mod


class Url:
    url_str = None
    view_or_sub_router = None
    router_obj_name = "routers"
    prefix = None

    def __init__(self, url_str, view_or_sub_router, router_obj_name="routers", prefix=None):
        self.url_str = url_str
        self.view_or_sub_router = view_or_sub_router
        self.router_obj_name = router_obj_name
        self.prefix = prefix


def make_url(url_str, view_or_sub_router, router_obj_name="routers", prefix=None):
    return Url(url_str, view_or_sub_router, router_obj_name, prefix)


class RouterMapper(dict):

    def load_urls_from_module(self, url_module_str, router_obj_name="routers"):
        url_module = mod.import_module_string(url_module_str)
        if hasattr(url_module, router_obj_name):
            routers = getattr(url_module, router_obj_name)
            if isinstance(routers, (list, tuple)):
                self.__load_routers(routers)

    def __load_routers(self, routers):
        for url in routers:
            self.add_router(url)

    def add_router(self, url: Url):
        if isinstance(url.view_or_sub_router, str):
            self.load_urls_from_module(url_module_str=url.view_or_sub_router, router_obj_name=url.router_obj_name)
        else:
            if url in self.keys():
                raise
            self.update({f"{url.prefix}{url.url_str}": url.view_or_sub_router})
