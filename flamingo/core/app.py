import warnings
from flamingo.core import g
from flamingo.middleware import base as middleware_base
from flamingo.plugins import base as plugin_base
from flamingo.conf.settings import settings
from flamingo.utils import functions
from flamingo.utils import wrap_funcs
from flamingo.utils import exc
from flamingo.utils import constant
from flamingo.url import mapper
from flamingo.io import response
from flamingo.plugins import base


class Flamingo:
    """
    Flamingo（火烈鸟）

    :param load_plugins: 是否加载配置中的插件
    :param load_middlewares: 是否加载配置中的中间件
    """

    def __init__(self, load_plugins=True, load_middlewares=True):
        self.load_plugins = load_plugins
        self.load_middlewares = load_middlewares
        # Request class
        self.request_class = None

        # Response class
        self.response_class = None

        # 初始化路由表
        self.router_mapper = mapper.RouterMapper()

        # Settings
        self.settings = None

        # 第一次请求标志位
        self._before_first_request = False

        # Middleware object list
        self.middlewares = []

    @classmethod
    def create_app(cls, load_plugins=True, load_middlewares=True):
        """
        创建应用

        :param load_plugins: if load_plugins is true, will setup all plugins
        :param load_middlewares: If true, will add middleware funcs to
        :return:
        """
        ins = cls(load_plugins=load_plugins, load_middlewares=load_middlewares)
        # 初始化应用
        ins.init_app()
        return ins

    def init_app(self):
        # 加载配置
        self.settings = settings

        # 加载路由
        self.router_mapper.load_url_from_conf(self.settings.CONF_URL)

        # 加载插件
        if self.load_plugins:
            self.__load_plugins_from_settings()

        # 加载中间件
        if self.load_middlewares:
            self.__load_middlewares_from_settings()

        # 加载请求类
        self.request_class = functions.load_class(self.settings.REQUEST_CLASS)

        self._before_first_request = True

    def __load_middlewares_from_settings(self):
        """
        从配置文件中加载所有中间件
        :return:
        """
        middleware_list = self.settings.MIDDLEWARES
        for middleware_cls in middleware_list:
            self.register_middleware(middleware_cls=middleware_cls)

    def __load_plugins_from_settings(self):
        """
        从配置文件中加载所有插件
        :return:
        """
        plugins = self.settings.PLUGINS
        for name, plugin_cls in plugins.items():
            self.register_plugin(name=name, plugin_cls=plugin_cls)

    @wrap_funcs.before_first_request_required
    def register_middleware(self, middleware_cls):
        """
        注册中间件，必须在第一次请求之前进行注册，否则注册不成功
        :param middleware_cls: 基于BaseMiddleware的子类中间件
        :return:
        """
        if issubclass(middleware_cls, middleware_base.BaseMiddleware):
            self.middlewares.append(middleware_cls())
        else:
            warnings.warn(f"{middleware_cls.__name__} is not subclass of BaseMiddleware")

    @wrap_funcs.before_first_request_required
    def register_plugin(self, name, plugin_cls):
        """
        将插件注册到应用中，必须在第一次请求之前进行注册，否则注册不成功
        :param name:
        :param plugin_cls:
        :return:
        """
        if issubclass(plugin_cls, plugin_base.BasePlugin):
            if name in base.plugins.keys():
                pass
            if hasattr(self.settings, f"plugin_{name}_settings".upper()):
                plugin_settings = getattr(self.settings, f"plugin_{name}_settings".upper())
            else:
                plugin_settings = {}
            base.plugins[name] = plugin_cls().setup(**plugin_settings)

    async def all_dispatch_request(self):
        """
        处理所有的请求
        :return:
        """
        request = g.g_context.cur_stack(identity=g.GlobalContext.REQ_IDENTIFY)
        if request is None:
            raise exc.CoreError("Current request is None.")
        resp = None
        try:
            resp = await request.do_request()
        except exc.PageNotFoundError as e:
            resp = response.HttpResponse(content=str(e), status=constant.HttpStatus.HTTP_PAGE_NOT_FOUND)
        except exc.CoreError as e:
            resp = response.HttpResponse(content=str(e), status=constant.HttpStatus.HTTP_INTERVAL_ERROR)
        except exc.ViewError as e:
            resp = response.HttpResponse(content=str(e), status=constant.HttpStatus.HTTP_METHOD_DENIED)
        except Exception as e:
            resp = response.HttpResponse(content=str(e), status=constant.HttpStatus.HTTP_INTERVAL_ERROR)
        finally:
            return resp

    async def __call__(self, scope=None, receive=None, send=None):
        """
        自动调用方法，为了此方法适配了uvicorn服务框架使用

        :param scope: 请求帧内容，以字典的形式存在
        :param receive: 接收请求的channel频道
        :param send: 返回数据channel频道
        :return:
        """
        # 加载请求数据
        request = await self.request_class(self).load_data(data=scope, recv=receive)
        # 压入队列
        request.push()
        # 处理请求数据
        resp = await self.all_dispatch_request()
        await send({
            "type": "http.response.start",
            "status": resp.http_status,
            "headers": resp.headers
        })
        await send({
            "type": "http.response.body",
            "body": resp.content,
        })

    def get_router_mapper(self):
        """
        获取路由表
        :return:
        """
        return self.router_mapper
