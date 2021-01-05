# 全局的插件变量
plugins = {}


def get_plugin_ins(name):
    """
    获取插件对象
    :param name: [str] 插件名称
    :return: [Object] 插件对象
    """
    global plugins
    return plugins.get(name)



class BasePlugin:

    def setup(self, **kwargs):
        pass

    def release(self):
        pass

    def get_handler(self):
        pass
