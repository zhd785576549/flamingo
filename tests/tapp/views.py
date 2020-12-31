from flamingo.core import g

app = g.g_context.current_app()


async def test(request):
    print(request.path)
    return "aaaa"


async def params_test(request, *args, **kwargs):
    print(kwargs)
    print(args)
    print(app.settings)
    return "test finish!"
