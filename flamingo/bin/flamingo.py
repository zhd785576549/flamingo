import sys
from flamingo.command import manage


def execute_from_argv():
    manage.CommandManagement(argv=sys.argv).execute_from_argv()
