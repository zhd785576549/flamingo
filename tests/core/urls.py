from flamingo.url.conf import path


routers = [
    path(url="/test", view_func_or_module="tapp.urls", name="test")
]
