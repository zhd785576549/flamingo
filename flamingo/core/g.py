from werkzeug.local import LocalStack
from flamingo.utils import exc


class GlobalContext:

    APP_IDENTIFY = "app"
    REQ_IDENTIFY = "request"

    def __init__(self):
        self.__app_ctx_stack = LocalStack()
        self.__req_ctx_stack = LocalStack()
        self.__object_stack_dict = {
            "app": self.__app_ctx_stack,
            "request": self.__req_ctx_stack
        }

    def pop_stack(self, identity="app"):
        """
        获取线程安全的对象

        :param identity: 对象标识 app是应用，request是请求对象，其他值错误
        :return:
        """
        stack = self.__object_stack_dict.get(identity)
        if stack is None:
            raise exc.CoreError(f"Unknown identity name {identity}")
        stack.pop()

    def current_app(self):
        """
        获取当前应用对象
        :return:
        """
        top = self.__app_ctx_stack.top
        if top is None:
            raise exc.CoreError(f"Current app is empty.")
        return top

    def push_stack(self, obj, identity):
        """
        压入堆栈

        :param obj: 对象app或者request对象
        :param identity: 对象标识 app是应用，request是请求对象，其他值错误
        :return:
        """
        stack = self.__object_stack_dict.get(identity)
        if stack is None:
            raise exc.CoreError(f"Unknown identity name {identity}")
        stack.push(obj)

    def cur_stack(self, identity):
        """
        获取当前栈顶的对象信息
        :param identity: 对象标识 app是应用，request是请求对象，其他值错误
        :return:
        """
        stack = self.__object_stack_dict.get(identity)
        if stack is None:
            raise exc.CoreError(f"Unknown identity name {identity}")
        return stack.top


g_context = GlobalContext()
