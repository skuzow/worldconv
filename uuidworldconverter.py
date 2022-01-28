import os.path
import yaml

from utils.modify import modifyjson, modifyfolder
from utils.player import getplayermap

# mode selector
print('Type to what you want to convert: offline or online')
mode = str(input())

# opens, loads & closes config.yml
configfile = open('./config/config.yml')
config = yaml.safe_load(configfile)
configfile.close()

# gets playermap & starts with file changes
playermap = getplayermap(config, mode)
if not playermap.__sizeof__() == 0:
    # whitelist.json uuid changer
    modifyjson('whitelist.json', config, playermap)
    # ops.json uuid changer
    modifyjson('ops.json', config, playermap)
    # banned-players.json uuid changer
    modifyjson('banned-players.json', config, playermap)
    # /playerdata uuid changer
    modifyfolder('playerdata', config, playermap)
    # /stats uuid changer
    modifyfolder('stats', config, playermap)
    # /advancements uuid changer
    modifyfolder('advancements', config, playermap)
else:
    print('[whitelist.json] File not found, exiting...')
