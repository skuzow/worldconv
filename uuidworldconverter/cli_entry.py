import sys

from uuidworldconverter.utils import logger
from uuidworldconverter.core.config import Config
from uuidworldconverter.core.converter import Converter

__all__ = [
    'main'
]


def __offline(config):
    converter = Converter(config, 'offline')
    converter.start()


def __online(config):
    converter = Converter(config, 'online')
    converter.start()


def main():
    if len(sys.argv) == 2:
        arg = '__' + sys.argv[1]
        entry = getattr(sys.modules[__name__], arg, None)
        if entry is not None and entry not in __all__ and callable(entry):
            config = Config()
            config.start()
            entry(config.config)
        else:
            print(f'[{logger.ERROR}] Unknown argument provided: {arg[2:]}')
    else:
        prefix = f'python {sys.argv[0]}'
        print(f'[{logger.INFO}] {prefix} offline: Starts converter from online to offline')
        print(f'[{logger.INFO}] {prefix} online: Starts converter from offline to online')
