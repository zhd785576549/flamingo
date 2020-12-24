DEBUG = True

# Register this plugins in app, and contain as dict mapping in memory.
# Can get object by flamingo.current_app.get_plugin("plugin_name")
# By the way, the same name plugin will be overriding
PLUGINS = {
    # "db": "flamingo.plugins.db.sqlalchemy:FlamingoSqlalchemy"
}

MIDDLEWARES = []

# Application list
INSTALLED_APPS = []

# Root configure url module path
CONF_URL = "core.urls"

# Secret key for generating password
SECRET_KEY = ""

REQUEST_CLASS = "flamingo.io.request:Request"
