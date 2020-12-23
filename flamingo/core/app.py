class RequestHandler:

    async def __call__(self, scope, receive, send):
        """
        Instant call method for uvicorn web server

        :param scope: A dictionary containing information about the incoming connection
        :param receive: A channel on which to receive incoming messages from the server
        :param send: A channel on which to send outgoing messages to the server
        :return:
        """
        print(scope)
        print(receive)
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/plain'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': b'Hello, world!',
        })
