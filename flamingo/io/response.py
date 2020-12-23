class Response:

    http_status = None
    headers = {}
    content = b""

    def __init__(self, request):
        self.request = request
