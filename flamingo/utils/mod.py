from importlib import import_module


def import_module_string(mod_str: str):
    """
    Import module string
    :param mod_str: [str] Module path
    :return: Module
    """
    mod = import_module(mod_str)
    return mod
