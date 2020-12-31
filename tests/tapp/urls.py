from . import views
from flamingo.url.url_conf import url


routers = [
    url(path="/aaaa", view_func=views.test, name="test_aaaa"),
    url(path="/params/<int:id>/", view_func=views.params_test)
]
