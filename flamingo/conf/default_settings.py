DEBUG = True

# Register this plugins in app, and contain as dict mapping in memory.
# Can get object by flamingo.current_app.get_plugin("plugin_name")
# By the way, the same name plugin will be overriding
PLUGINS = {
    "db": "flamingo.plugins.db.sqlalchemy:FlamingoSqlalchemy"
}

SERVER_NAME = None

MIDDLEWARES = []

# Application list
INSTALLED_APPS = []

# Root configure url module path
CONF_URL = ""

# Secret key for generating password
SECRET_KEY = ""

REQUEST_CLASS = "flamingo.io.request:Request"


RESPONSE_CLASS = "flamingo.io.response:Response"
