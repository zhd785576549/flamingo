from werkzeug.formparser import FormDataParser, default_stream_factory
from werkzeug.http import parse_options_header
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.urls import url_decode
from typing import Any
from io import BytesIO
import json
from flamingo.utils import functions


class BaseParser:
    parameter_storage_class = ImmutableMultiDict
    max_content_length = None
    encoding_errors = "replace"
    max_form_memory_size = None

    def __init__(self, receiver=None, headers=None, charset="utf-8", scope=None):
        self.__receiver = receiver
        self.__headers = headers
        self.__charset = charset
        self.__scope = scope

    @property
    def query_string(self):
        return self.__scope.query_string if self.__scope else ""

    @property
    def receiver(self):
        return self.__receiver

    @property
    def headers(self):
        return self.__headers

    @property
    def charset(self):
        return self.__charset

    def parse(self) -> Any:
        raise NotImplementedError


class FormParser(BaseParser):
    form_parser_class = FormDataParser

    async def parse(self):
        """
        将请求的数据转化为相应的数据格式
        :return:
        """
        parser_func_dict = {
            "application/json": self._parse_json_data
        }
        content_type = self.headers.get("content-type", "application/json")
        content_length = int(self.headers.get("content-length", 0))
        # 处理正文格式，如果是multipart/form-data，将boundary等信息放在options里
        mimetype, options = parse_options_header(content_type)
        # JSON数据格式使用自定义的处理方式
        parse_func = parser_func_dict.get(mimetype, self._parse_form_data)
        return await parse_func(mimetype, content_length, options)

    async def _parse_form_data(self, mimetype, content_length, options):
        """
        匹配Form表单请求

        :param mimetype: 请求数据格式
        :param content_length: 数据长度
        :param options: 选项
        :return:
        """
        parser = self.form_parser_class(
            self._get_file_stream,
            self.charset,
            self.encoding_errors,
            self.max_form_memory_size,
            self.max_content_length,
            self.parameter_storage_class,
            # False
        )
        return parser.parse(await self._get_stream(), mimetype, content_length, options)

    async def _parse_json_data(self, mimetype, content_length, options):
        """
        匹配JSON请求

        :param mimetype: 请求数据格式
        :param content_length: 数据长度
        :param options: 选项
        :return:
        """
        body_data = await functions.read_body(receive=self.receiver)
        data = json.loads(body_data.decode(encoding=self.charset))
        return None, ImmutableMultiDict(data), ImmutableMultiDict()

    def _get_file_stream(self, total_content_length, content_type, filename=None, content_length=None):
        return default_stream_factory(
            total_content_length=total_content_length,
            filename=filename,
            content_type=content_type,
            content_length=content_length,
        )

    async def _get_stream(self):
        """
        获取请求输入流
        :return:
        """
        body_data = await functions.read_body(receive=self.receiver)
        # 为了匹配werkzeug的输入流方式，只是简单的做了数据类型的转换，转成BytesIO的形式
        # 如果请求的数据量很大，容易引发内容崩溃的情况
        # TODO 需要做成receive()流的形式，异步进行处理数据，werkzeug的数据流是基于wsgi的需要改造
        _stream = BytesIO()
        _stream.write(body_data)
        _stream.seek(0)
        return _stream


class ParseQueryParser(BaseParser):

    def parse(self):
        return url_decode(
            self.query_string,
            self.charset,
            errors=self.encoding_errors,
            cls=self.parameter_storage_class
        )
