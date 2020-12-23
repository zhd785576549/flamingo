import uvicorn
from flamingo.core import app
from flamingo.utils import logo
from flamingo.command import base


class Command(base.BaseCommand):

    def add_argument(self, parser):
        parser.add_argument("--host", type=str, dest="host", required=False, default="127.0.0.1")
        parser.add_argument("--port", type=int, dest="port", required=False, default=8888)
        parser.add_argument("--enable-log-color", type=bool, dest="bo_color", required=False, default=False)
        parser.add_argument("--enable-reload", type=bool, dest="bo_reload", required=False, default=False)

    def handle(self, *args, **options):
        host = options.get("host")
        port = options.get("port")
        bo_color = options.get("bo_color")
        bo_reload = options.get("bo_reload")
        logo.display_logo()
        uvicorn.run(app=app.RequestHandler(), host=host, port=port, use_colors=bo_color, reload=bo_reload)
