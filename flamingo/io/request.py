from flamingo.core import app
from flamingo.core import g
from flamingo.io import response
from flamingo.utils import functions
from flamingo.utils import exc


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

    def load_data(self, data):
        """
        加载Scope数据
        :param data: [dict] 等待加载的数据
        :return:
        """
        self.__trans_scope_to_request(data)
        return self

    def __trans_scope_to_request(self, scope):
        """
        将Uvicorn的数据转换成request的内部数据

        :param scope: [dict] Uvicorn的请求数据
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
        # 请求数据
        self.data = functions.trans_str_to_dict(scope_ins.data)
        self.params = functions.trans_str_to_dict(scope_ins.query_string)
        self.files = functions.trans_str_to_dict(scope_ins.files)
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

    def do_request(self):
        """
        执行请求，并且返回对应的数据
        :return:
        """
        # 获取URL MAPPING路由对应的View类
        view_func, kwargs, args, find = self.get_app().router_adapter.test(path=self.path)
        if view_func:  # 执行对应的方法，并且返回对应的数据
            if callable(view_func):
                resp = view_func(self, *args, **kwargs)
                if isinstance(resp, str):
                    return response.HttpResponse(content=resp).encode()
                elif isinstance(resp, dict):
                    return response.JsonResponse(content=resp).encode()
                elif isinstance(resp, response.BaseResponse):
                    return resp
            else:
                raise exc.ViewError("View func is an unknown type object.")
        else:  # 未找到返回404状态
            raise exc.PageNotFoundError

    def push(self):
        top = g.g_context.cur_stack(identity=g.GlobalContext.REQ_IDENTIFY)
        if top is not None and top.preserved:
            top.pop(top._preserved_exc)
        g.g_context.push_stack(self, identity=g.GlobalContext.REQ_IDENTIFY)

    def pop(self):
        pass
