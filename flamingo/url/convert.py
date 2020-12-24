import datetime


class BaseConvert:

    def __init__(self, value, reg=None):
        self.__value = value
        self.__reg = reg

    def get_value(self):
        raise NotImplementedError

    @property
    def value(self):
        return self.__value

    @property
    def regex(self):
        return self.__reg


class IntegerConvert(BaseConvert):

    def __init__(self, value):
        super(IntegerConvert, self).__init__(value=value, reg=r"\d+")

    def get_value(self):
        return int(self.value)


class StringConvert(BaseConvert):

    def __init__(self, value):
        super(StringConvert, self).__init__(value=value, reg=r".*")

    def get_value(self):
        return str(self.value)


class FloatConvert(BaseConvert):

    def __init__(self, value):
        super(FloatConvert, self).__init__(value=value, reg=r"\d+.\d+")

    def get_value(self):
        return str(self.value)


class DateTimeConvert(BaseConvert):

    def __init__(self, value, fmt="%Y-%m-%d", reg=r"\d+-\d+-\d+"):
        super(DateTimeConvert, self).__init__(value=value, reg=reg)
        self.fmt = fmt

    def get_value(self):
        return datetime.datetime.strptime(self.value, self.fmt)
