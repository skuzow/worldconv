import json
import logging
import os

from uuidworldconverter.utils import logger
from uuidworldconverter.core.modify import Modify
from uuidworldconverter.utils import uuid


class Converter:

    def __init__(self, config, mode):
        self.__config = config
        self.__mode = mode
        # __uuid_map -> search_uuid : [ change_uuid, player_name ]
        self.__uuid_map = {}
        # __player_list -> player_name
        self.__player_list = []

    def start(self):
        # checks mojang api status, or internet connection
        if uuid.generate_online('legendh', True):
            print(f'[{logger.INFO}] Mojang api working, so continues!')
        else:
            return print(f'[{logger.ERROR}] Mojang api not working, or not internet connection, exiting...')
        # checks if server folder exists, if it doesn't create it
        server_path = os.path.join(os.getcwd(), self.__config["server_directory"])
        if not os.path.isdir(server_path):
            os.mkdir(server_path)
            return print(f'[{logger.WARNING}] Server folder successfully created so its but empty :(, exiting...')
        elif not os.listdir(server_path):
            return print(f'[{logger.ERROR}] Server folder is empty!, place your server inside it, exiting...')
        print(f'[{logger.INFO}] Starting converting with mode {self.__mode} selected')
        # generates __uuid_map with recollecting json file information
        for file in self.__config["files"]:
            self.__generate_player_map(file)
        # if __uuid_map have stuff inside continues
        if self.__uuid_map.__sizeof__() == 0:
            print(f'[{logger.ERROR}] Obtainable uuid files not found, exiting...')
        else:
            # prints "pretty" __uuid_map
            print(f'[{logger.INFO}] [player_map] {json.dumps(self.__uuid_map, indent=4)}')
            # modify
            modify = Modify(self.__config, self.__uuid_map)
            # files uuid changer
            for file in self.__config["files"]:
                modify.modify_json(file)
            # folder uuid changer
            for folder in self.__config["folders"]:
                modify.modify_folder(folder)

    def __generate_player_map(self, file_name):
        file_path = os.path.join(os.getcwd(), self.__config["server_directory"], file_name["name"])
        # if file_name doesn't exist, returns with error print
        if not os.path.isfile(file_path):
            return print(f'[{logger.ERROR}] [{file_name["name"]}] File not found in: {file_path}')
        try:
            # open, loads & closes file_name in read mode
            file = open(file_path, 'r')
            file_json = json.load(file)
            file.close()
            # for each in file_json
            for player in file_json:
                # checks first if player is inside __player_map
                if player["name"] not in self.__player_list:
                    self.__player_list.append(player["name"])
                    # checks if name for getting online uuid is valid
                    online_uuid = uuid.generate_online(player["name"], False)
                    if online_uuid:
                        offline_uuid = uuid.generate_offline(player["name"])
                        if self.__mode == 'offline' and online_uuid not in self.__uuid_map:
                            self.__uuid_map[online_uuid] = [offline_uuid, player["name"]]
                        elif self.__mode == 'online' and offline_uuid not in self.__uuid_map:
                            self.__uuid_map[offline_uuid] = [online_uuid, player["name"]]
                    else:
                        print(f'[{logger.WARNING}] [{file_name["name"]}] {player["name"]} could not be found as a premium username')
                else:
                    print(f'[{logger.INFO}] [{file_name["name"]}] {player["name"]} already in player_list')
            return self.__uuid_map
        except Exception as e:
            logging.exception(e)
            print(f'[{logger.ERROR}] [{file_name["name"]}] Could not load file for getting information in: {file_path}')
