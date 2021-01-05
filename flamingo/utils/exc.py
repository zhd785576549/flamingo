class FlamingoError(Exception):
    pass


class ClassNotFoundError(FlamingoError):
    pass


class ViewError(FlamingoError):
    pass


class PageNotFoundError(ViewError):
    pass


class ConfigureError(FlamingoError):
    pass


class ImproperlyConfigured(FlamingoError):
    pass


class CoreError(FlamingoError):
    pass


class CommandError(FlamingoError):
    pass
