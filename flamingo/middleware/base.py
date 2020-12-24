class BaseMiddleware:
    """
    中间件基类，自定义的中间件都必须继承这个基类
    """

    def before_request(self, request):
        """
        每次请求后在调用用户自定义方法之前调用该方法
        :param request: 请求对象
        :return:
        """
        raise NotImplementedError()

    def before_response(self, response):
        """
        在自定义方法返回之后需要进一步处理返回数据。
        重写此方法，需要返回response对象，若返回None则沿用上次response的对象

        :param response: 返回对象
        :return:
        """
        raise NotImplementedError()
