import re
from flamingo.url import url_conf
from flamingo.url import convert


class BaseUrlAdapter:

    def __init__(self, url_mapper: url_conf.UrlMapper):
        self.__mapper = url_mapper

    def test(self, path):
        raise NotImplementedError

    @property
    def mapper(self):
        return self.__mapper


class RegexUrlAdapter(BaseUrlAdapter):

    def test(self, path):
        """
        遍历校验所有的路由，并且返回成功的路由参数和方法名称

        :param path: 请求路由
        :return: (view方法, 字典路由参数, 列表路由参数, 是否匹配到路由)
        """
        for pattern, func_name in self.mapper.get_url_mapper():
            # 优先使用用户自定义的匹配方法，如果没有配置，使用RegularUrlPattern类
            url_patter = self.mapper.get_url_pattern(func_name=func_name) or RegularUrlPattern(pattern=pattern)
            kwargs, args, find = url_patter.match(path)
            if find:
                view_func = self.mapper.get_view_func(func_name=func_name)
                return view_func, kwargs, args, find
        return None, {}, [], False


class BaseUrlPattern:

    def __init__(self, pattern):
        self.__pattern = pattern

    @property
    def pattern(self):
        return self.__pattern

    def match(self, root_path):
        pass


class RegularUrlPattern(BaseUrlPattern):

    CONVERT_DICT = {
        "int": convert.IntegerConvert,
        "string": convert.StringConvert,
        "float": convert.FloatConvert
    }

    def match(self, path):
        path_list = re.findall(r"[^/]+", path)
        pattern_list = re.findall(r"[^/]+", self.pattern)
        if len(pattern_list) == len(path_list):
            kwargs = {}
            args = []
            for index, pattern_item in enumerate(pattern_list):
                if pattern_item == path_list[index]:
                    continue
                else:
                    r = re.match(r"<(?P<convert_type>.*?):(?P<convert_value>.*?)>", pattern_item)
                    if r:
                        g = r.groupdict()
                        convert_type = g.get("convert_type")
                        convert_value = g.get("convert_value")
                        if convert_type and convert_value:
                            c = self.CONVERT_DICT.get(convert_type)
                            if issubclass(c, convert.BaseConvert):
                                key = convert_value
                                val = c(path_list[index]).get_value()
                                kwargs.update({key: val})
                                args.append(val)
                            else:
                                return {}, [], False
                        else:
                            return {}, [], False
                    else:
                        return {}, [], False
            return kwargs, args, True
        else:
            return {}, [], False
