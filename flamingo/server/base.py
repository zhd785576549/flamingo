class BaseServer:

    def __init__(self, app, **kwargs):
        """
        Construct method
        """
        self.kwargs = kwargs
        self.app = app

    def run_serve(self):
        raise NotImplementedError
