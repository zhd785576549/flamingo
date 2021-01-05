from werkzeug.exceptions import NotFound
from flamingo.core import app
from flamingo.core import g
from flamingo.io import response
from flamingo.utils import functions
from flamingo.utils import exc
from flamingo.utils import constant


class Scope:

    @classmethod
    def from_dict(cls, scope: dict):
        ins = cls()
        for k, v in scope.items():
            ins.__dict__[k] = v
        return ins

    def __getattr__(self, item):
        return self.__dict__.get(item)


class BaseRequest:

    def __init__(self, application: app.Flamingo, **kwargs):
        self.__app = application
        self.kwargs = kwargs
        self.req_type = None
        self.http_version = None
        self.host = None
        self.client_ip = None
        self.scheme = None
        self.method = None
        self.root_path = None
        self.path = None
        self.raw_path = None
        self.params = None
        self.data = None
        self.files = None
        self.headers = None
        self.cookies = None

    def load_scope(self, scope):
        pass

    def get_app(self):
        return self.__app


class Request(BaseRequest):

    def __init__(self, application: app.Flamingo, **kwargs):
        super(Request, self).__init__(application=application, **kwargs)
        self.preserved = False
        self._preserved_exc = None
        self.__url_adapter = None

    async def load_data(self, data, recv=None):
        """
        加载Scope数据
        :param data: [dict] 等待加载的数据
        :param recv: 接收的数据
        :return:
        """
        await self.__trans_scope_to_request(data, recv)
        return self

    async def __trans_scope_to_request(self, scope, recv=None):
        """
        将Uvicorn的数据转换成request的内部数据

        :param scope: [dict] Uvicorn的请求数据
        :param recv: 接受数据
        :return:
        """
        scope_ins = Scope.from_dict(scope=scope)
        # 请求类型 http
        self.req_type = scope_ins.type
        # 请求方法
        self.method = scope_ins.method
        # 请求路由
        self.path = scope_ins.path
        self.root_path = scope_ins.root_path
        self.raw_path = scope_ins.raw_path
        # 路由参数
        self.params = functions.trans_params_to_dict(scope_ins)
        # 请求头 和 请求Cookie
        self.headers = functions.trans_headers(scope_ins.headers)
        # 请求的http版本号
        self.http_version = scope_ins.http_version
        # 请求协议http还是https
        self.scheme = scope_ins.scheme
        # 请求客户端IP地址
        self.client_ip = scope_ins.client[0]
        # 请求主机IP或者HOST名称
        self.host = scope_ins.server[0]

        # 解析请求数据
        if self.method.upper() in [constant.RequestMethod.RM_POST, constant.RequestMethod.RM_PUT]:
            stream, self.data, self.files = await functions.trans_body_data(receiver=recv, headers=self.headers)

        # 初始化 SERVER_NAME，如果没有设置SERVER_NAME，那么默认使用HOST:PORT作为SERVER_NAME
        if self.get_app().settings.SERVER_NAME is None:
            self.get_app().settings.SERVER_NAME = f"{scope_ins.server[0]}:{scope_ins.server[1]}"

        # 初始化路由适配
        mapper = self.get_app().router_mapper.mapper
        self.__url_adapter = self.get_app().router_mapper.mapper.bind(
            server_name=self.get_app().settings.SERVER_NAME,
            subdomain=mapper.default_subdomain or None,
            url_scheme=self.scheme,
            query_args=self.params,
            path_info=self.path
        )

    async def do_request(self):
        """
        执行请求，并且返回对应的数据
        :return:
        """
        try:
            # 匹配理由表
            name, args = self.__url_adapter.match()
            # 获取视图方法
            view_func = self.get_app().router_mapper.get_view_func(name=name)
            # 执行对应的方法，并且返回对应的数据
            if view_func:
                if callable(view_func):
                    resp = await view_func(self, **args)
                    if isinstance(resp, str):
                        return response.HttpResponse(content=resp).encode()
                    elif isinstance(resp, dict):
                        return response.JsonResponse(content=resp).encode()
                    elif isinstance(resp, response.BaseResponse):
                        return resp
                else:
                    # 视图方法不能被执行
                    raise exc.ViewError("View func is an unknown type object.")
            else:
                # 未找到对应的视图方法
                raise exc.ViewError()
        except NotFound as e:
            # 未找到对应的路由
            raise exc.PageNotFoundError(e)

    def push(self):
        top = g.g_context.cur_stack(identity=g.GlobalContext.REQ_IDENTIFY)
        if top is not None and top.preserved:
            top.pop(top._preserved_exc)

        _app = g.g_context.cur_stack(identity=g.GlobalContext.APP_IDENTIFY)
        if _app is None or _app != self.get_app():
            g.g_context.push_stack(self.get_app(), identity=g.GlobalContext.APP_IDENTIFY)

        g.g_context.push_stack(self, identity=g.GlobalContext.REQ_IDENTIFY)

    def pop(self):
        pass
