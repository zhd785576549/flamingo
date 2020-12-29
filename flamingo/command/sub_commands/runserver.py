from flamingo.utils import logo
from flamingo.command import base
from flamingo.server import servers
from flamingo import Flamingo


class Command(base.BaseCommand):

    def add_argument(self, parser):
        parser.add_argument("--host", type=str, dest="host", required=False, default="127.0.0.1")
        parser.add_argument("--port", type=int, dest="port", required=False, default=8888)
        parser.add_argument("--enable-log-color", type=bool, dest="use_colors", required=False, default=False)
        parser.add_argument("--enable-reload", type=bool, dest="reload", required=False, default=False)

    def handle(self, *args, **options):
        logo.display_logo()
        app = Flamingo()
        app.init_app()
        server = servers.UvicornServer(app=app, **options)
        server.run_serve()
