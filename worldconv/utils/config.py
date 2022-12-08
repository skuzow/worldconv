import logging
import os
import ruamel.yaml

from worldconv.utils import logger


path: str = os.path.join(os.getcwd(), 'config.yml')
config: str = ""
default_config: str = """\
# Config file for worldconv
# https://github.com/skuzow/worldconv

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


def load() -> bool:
    yaml = ruamel.yaml.YAML()
    # if config exists it loads it
    if os.path.exists(path):
        config_file = open(path)
        config = yaml.load(config_file)
        config_file.close()
        return False
    # else creates it with default_config
    else:
        yaml = ruamel.yaml.YAML()
        config = yaml.load(default_config)
        try:
            # opens config in append mode
            config_file = open(path, 'a')
            # dumps info inside
            yaml.dump(config, config_file)
            config_file.close()
            logger.info('''Config file created successfully, take a look to
                        change configuration if you need it''')
            return True
        except Exception as e:
            logging.exception(e)
            logger.error('There was a problem saving default config file')
            return True
