# utils/config.py
import configparser
import os

class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolação que permite o uso de variáveis de ambiente."""
    def before_get(self, parser, section, option, value, defaults):
        return os.path.expandvars(value)

def get_config():
    config = configparser.ConfigParser(interpolation=EnvInterpolation())
    config.read('config.ini')
    return config
