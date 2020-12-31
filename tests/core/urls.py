from flamingo.url.url_conf import url


routers = [
    url(path="/test", view_func="tapp.urls", name="test")
]
