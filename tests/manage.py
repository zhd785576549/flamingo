import os
from flamingo.bin.flamingo import execute_from_argv

if __name__ == '__main__':
    os.environ["FLAMINGO_SETTINGS_MODULE"] = "core.settings"
    execute_from_argv()
