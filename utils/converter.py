import json
import os

from utils.modify import Modify
from utils.uuid import Uuid


class Converter:

    def __init__(self, config, mode):
        self.__config = config
        self.__mode = mode
        self.__uuid = Uuid()
        # __player_map -> search_uuid : [ change_uuid, player_name ]
        self.__player_map = {}

    def start(self):
        # generates __player_map with recollecting json file information
        for file in self.__config['files']:
            self.__generate_player_map(file)
        # if __player_map have stuff inside continues
        if self.__player_map.__sizeof__() == 0:
            print('[ERROR] Obtainable uuid files not found, exiting...')
        else:
            # prints "pretty" __player_map
            print('[player_map] {}'.format(json.dumps(self.__player_map, indent=4)))
            # modify
            modify = Modify(self.__config, self.__player_map)
            # files __uuid changer
            for file in self.__config['files']:
                modify.modify_json(file)
            # folder __uuid changer
            for folder in self.__config['folders']:
                modify.modify_folder(folder)

    def __generate_player_map(self, file_name):
        file_path = os.path.join(self.__config['server_directory'], file_name["name"])
        # if file_name doesn't exist, returns with error print
        if not os.path.isfile(file_path):
            return print(f'[{file_name["name"]}] ERROR not found')
        # open, loads & closes file_name in read mode
        file = open(file_path, 'r')
        file_json = json.load(file)
        file.close()
        # for each in file_json
        for player in file_json:
            try:
                if self.__mode == 'offline':
                    online_uuid = self.__uuid.generate_online(player['name'])
                    if online_uuid not in self.__player_map:
                        self.__player_map[online_uuid] = [self.__uuid.generate_offline(player['name']), player['name']]
                elif self.__mode == 'online':
                    offline_uuid = self.__uuid.generate_offline(player['name'])
                    if offline_uuid not in self.__player_map:
                        self.__player_map[offline_uuid] = [self.__uuid.generate_online(player['name']), player['name']]
            except:
                print(f'[{file_name["name"]}] {player["name"]} could not be found as a premium username')
        return self.__player_map
