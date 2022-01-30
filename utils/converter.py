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
        self.__generate_player_map()
        if self.__player_map.__sizeof__() == 0:
            print('[ERROR] Obtainable __uuid files not found, exiting...')
        else:
            modify = Modify(self.__config, self.__player_map)
            # files __uuid changer
            for file in self.__config['files']:
                modify.modify_json(file)
            # folder __uuid changer
            for folder in self.__config['folders']:
                modify.modify_folder(folder)

    def __generate_player_map(self):
        # whitelist
        whitelist_path = os.path.join(self.__config['server_directory'], self.__config['files'][0]['name'])
        # checks if whitelist.json exists, if it doesn't it exits with __player_map.__sizeof__() = 0
        if not os.path.isfile(whitelist_path):
            print('[whitelist.json] ERROR not found')
            return self.__player_map
        # open, loads & closes whitelist.json in read mode
        whitelist_file = open(whitelist_path, 'r')
        whitelist = json.load(whitelist_file)
        whitelist_file.close()
        # for each in whitelist.json
        for player in whitelist:
            try:
                offline_uuid = self.__uuid.generate_offline(player['name'])
                online_uuid = self.__uuid.generate_online(player['name'])
                if self.__mode == 'offline':
                    self.__player_map[online_uuid] = [offline_uuid, player['name']]
                elif self.__mode == 'online':
                    self.__player_map[offline_uuid] = [online_uuid, player['name']]
            except:
                print('[whitelist.json] {} could not be found as a premium username'.format(player['name']))
        # ops
        self.__check_file('ops.json')
        # banned-players
        self.__check_file('banned-players.json')
        # prints "pretty" __player_map
        print('[__player_map] {}'.format(json.dumps(self.__player_map, indent=4)))
        return self.__player_map

    def __check_file(self, file_name):
        file_path = os.path.join(self.__config['server_directory'], file_name)
        if not os.path.isfile(file_path):
            return print(f'[{file_name}] ERROR not found')
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
                print(f'[{file_name}] {player["name"]} could not be found as a premium username')
