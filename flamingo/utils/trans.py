from flamingo.utils import constant


class BaseTransfer:

    def __init__(self, data, **kwargs):
        self.__data = data

    @property
    def data(self):
        return self.__data

    def trans(self) -> dict:
        raise NotImplementedError


class FormDataTransfer(BaseTransfer):

    def trans(self) -> dict:
        pass


class JsonDataTransfer(BaseTransfer):

    def trans(self) -> dict:
        pass


class FormBoundaryTransfer(BaseTransfer):

    def trans(self) -> dict:
        print(self.data)
        return {}


def get_trans_dict(content_type, data, boundary, decoding="UTF-8"):
    """
    获取转换之后的数据

    :param content_type: 内容的类型
    :param boundary: 分割标识
    :param decoding: 解码格式
    :param data: 请求的数据
    :return:
    """
    content_cls_dict = {
        constant.ContentType.CT_JSON: JsonDataTransfer,
        constant.ContentType.CT_FROM_DATA: FormDataTransfer,
        constant.ContentType.CT_FORM_URLENCODED: FormBoundaryTransfer
    }
    cls = content_cls_dict.get(content_type)
    if cls and issubclass(cls, BaseTransfer):
        return cls(data, boundary=boundary, decoding=decoding).trans()
    else:
        return {}


