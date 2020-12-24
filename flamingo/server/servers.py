import uvicorn
from flamingo.server import base


class UvicornServer(base.BaseServer):
    """
    Uvicorn async server class, start a uvicorn fast server
    """

    def run_serve(self):
        uvicorn.run(app=self.app, **self.kwargs)
