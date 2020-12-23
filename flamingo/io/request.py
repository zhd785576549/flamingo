from flamingo.io import response


class RequestParams:
    req_type = None
    req_http_version = None


class Request:

    def __init__(self, *args, **kwargs):
        self.params = RequestParams()

    def load_scope(self, scope: dict):
        self.params.req_type = scope.get("type")
        return self

    def to_response(self):
        resp = response.Response(request=self)
        return resp


class RequestHandler:
    request_class = Request

    async def __call__(self, scope, receive, send):
        """
        Instant call method for uvicorn web server

        :param scope: A dictionary containing information about the incoming connection
        :param receive: A channel on which to receive incoming messages from the server
        :param send: A channel on which to send outgoing messages to the server
        :return:
        """
        # print(receive)
        # Load request
        request = self.request_class().load_scope(scope=scope)
        # Deal request with url mapper
        resp = request.to_response()
        # Response to client
        await send({
            "type": "http.response.start",
            "status": resp.http_status,
            "headers": resp.headers
        })

        await send({
            "type": "http.response.body",
            "body": resp.content
        })
