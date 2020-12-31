from flamingo.core import g


async def test(request):
    print(request.path)
    return "aaaa"


async def params_test(request, *args, **kwargs):
    print(kwargs)
    print(args)
    print("Request params : ", request.params)
    print("Request data: ", request.data)
    print("Request files: ", request.files)
    print(g.g_context.current_app().settings.DEBUG)
    return "test finish!"
