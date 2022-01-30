import yaml

from utils.converter import Converter

# __mode selector
print('Type to what you want to convert: offline or online')
mode = str(input())

# opens, loads & closes __config.yml
configfile = open('./config/config.yml')
config = yaml.safe_load(configfile)
configfile.close()

# gets __player_map & starts with file changes
converter = Converter(config, mode)
converter.start()
