import json
from flamingo.utils import constant


class BaseResponse:

    def __init__(self, content, status=constant.HttpStatus.HTTP_OK, headers=None):
        self.__content = content
        self.__status = status
        if headers:
            self.__headers = headers
        else:
            self.__headers = []

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, c):
        self.__content = c

    @property
    def http_status(self):
        return self.__status

    @property
    def headers(self):
        return self.__headers

    def encode(self):
        raise NotImplementedError


class HttpResponse(BaseResponse):

    def encode(self, encoding="UTF-8"):
        if isinstance(self.content, bytes):
            return self
        if isinstance(self.content, str):
            self.content = self.content.encode(encoding=encoding)
            return self
        else:
            raise


class JsonResponse(BaseResponse):
    def encode(self, encoding="UTF-8"):
        if isinstance(self.content, dict):
            self.content = json.dumps(self.content).encode(encoding=encoding)
            return self
        else:
            raise


