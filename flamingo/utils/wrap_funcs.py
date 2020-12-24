def before_first_request_required(func):
    def deco(self, *args, **kwargs):
        if self._before_first_request is True:
            func(*args, **kwargs)
        else:
            raise
    return deco
