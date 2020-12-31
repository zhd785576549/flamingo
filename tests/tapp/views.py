
def test(request):
    print(request.path)
    return "aaaa"


def params_test(request, *args, **kwargs):
    print(kwargs)
    print(args)
    return "test finish!"
