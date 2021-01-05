from flamingo.core import g


async def test(request):
    print(request.path)
    return "aaaa"


async def params_test(request, **kwargs):
    print("Request path params : ", kwargs)
    print("Request params : ", request.params)
    print("Request data: ", request.data)
    print("Request files: ", request.files)
    return {
        "code": 100200,
        "message": "Test OK"
    }
