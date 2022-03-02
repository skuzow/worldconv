import logging
import os
import ruamel.yaml

from uuidworldconverter.utils import logger

yaml_str = """\
# Config file for uuid-world-converter
# https://github.com/legendnightt/uuid-world-converter

# Server Directory
server_directory: server

# World Directory
world_directory: world

# Changing /server uuids
# IMPORTANT: used for getting player names for obtaining uuids
files:
  - name: usercache.json
    enable: true
  - name: whitelist.json
    enable: true
  - name: ops.json
    enable: true
  - name: banned-players.json
    enable: true

# Changing /world uuids
folders:
  - name: playerdata
    enable: true
  - name: stats
    enable: true
  - name: advancements
    enable: true
"""


class Config:

    def __init__(self):
        self.__path = os.path.join(os.getcwd(), 'config.yml')
        self.config = ""

    def start(self):
        yaml = ruamel.yaml.YAML()
        # if config exists it loads it
        if os.path.exists(self.__path):
            configfile = open(self.__path)
            self.config = yaml.load(configfile)
            configfile.close()
        # else creates it with yaml_str
        else:
            yaml = ruamel.yaml.YAML()
            self.config = yaml.load(yaml_str)
            try:
                # opens file_name in append mode
                configfile = open(self.__path, 'a')
                # dumps info inside
                yaml.dump(self.config, configfile)
                configfile.close()
                print(f'[{logger.INFO}] Config file created successfully, take a look to change configuration if you need it')
            except Exception as e:
                logging.exception(e)
                print(f'[{logger.ERROR}] There was a problem saving default config file')
