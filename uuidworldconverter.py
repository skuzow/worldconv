import yaml

from utils.converter import Converter

# mode selector
print('Type to what you want to convert: offline or online')
mode = str(input())

# opens, loads & closes config.yml
configfile = open('./config/config.yml')
config = yaml.safe_load(configfile)
configfile.close()

# gets player_map & starts with file changes
converter = Converter(config, mode)
converter.start()
