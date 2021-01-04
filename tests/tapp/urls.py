from . import views
from flamingo.url.conf import path


routers = [
    path(url="/aaaa", view_func_or_module=views.test, name="test_aaaa"),
    path(url="/params/<int:id>/", view_func_or_module=views.params_test)
]
