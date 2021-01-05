from flamingo.utils import exc


class BaseView:
    allow_methods = ["GET", "POST", "DELETE", "PUT", "HEADER", "OPTION"]

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def dispatch_method(self, request, *args, **kwargs):
        if request.method.upper() in self.allow_methods:
            if hasattr(self, request.method.lower()):
                func = getattr(self, request.method.lower())
                if callable(func):
                    # 调用中间件对请求进行操作
                    middlewares = request.get_app().middlewares
                    for middleware in middlewares:
                        request = middleware.before_request(request=request)
                    # 执行用户请求
                    response = func(request, *args, **kwargs)
                    # 调用中间件对返回数据进行操作
                    for middleware in middlewares:
                        response = middleware.before_response(response=response)
                    return response
                else:
                    raise exc.ViewError("Method not callable.")
            else:
                raise exc.ViewError(f"Method {request.method} not allowed")
        else:
            raise exc.ViewError(f"Method {request.method} not allowed")

    @classmethod
    def as_view(cls, *args, **init_kwargs):
        def view(request, *args, **kwargs):
            self = cls(**init_kwargs)
            return self.dispatch_method(request, *args, **kwargs)
        return view


class View(BaseView):
    pass
