import json
import logging
import os

from uuidworldconverter.core.modify import Modify
from uuidworldconverter.utils import uuid


class Converter:

    def __init__(self, config, mode):
        self.__config = config
        self.__mode = mode
        # __player_map -> search_uuid : [ change_uuid, player_name ]
        self.__player_map = {}

    def start(self):
        # checks mojang api status, or internet connection
        if uuid.generate_online('legendh'):
            print('[Mojang] Api working, so continues!')
        else:
            return print('[ERROR] Mojang api not working, or not internet connection, exiting...')
        # checks if server folder exists, if it doesn't create it
        server_path = os.path.join(os.getcwd(), self.__config["server_directory"])
        if not os.path.isdir(server_path):
            os.mkdir(server_path)
            return print('[WARNING] Server folder successfully created so its but empty :(, exiting...')
        elif not os.listdir(server_path):
            return print('[ERROR] Server folder is empty!, place your server inside it, exiting...')
        print(f'Starting converting with mode {self.__mode} selected')
        # generates __player_map with recollecting json file information
        for file in self.__config["files"]:
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
            for file in self.__config["files"]:
                modify.modify_json(file)
            # folder __uuid changer
            for folder in self.__config["folders"]:
                modify.modify_folder(folder)

    def __generate_player_map(self, file_name):
        file_path = os.path.join(os.getcwd(), self.__config["server_directory"], file_name["name"])
        # if file_name doesn't exist, returns with error print
        if not os.path.isfile(file_path):
            return print(f'[{file_name["name"]}] ERROR not found')
        try:
            # open, loads & closes file_name in read mode
            file = open(file_path, 'r')
            file_json = json.load(file)
            file.close()
            # for each in file_json
            for player in file_json:
                # checks first if name for getting online uuid is valid
                online_uuid = uuid.generate_online(player["name"])
                if online_uuid:
                    offline_uuid = uuid.generate_offline(player["name"])
                    if self.__mode == 'offline' and online_uuid not in self.__player_map:
                        self.__player_map[online_uuid] = [offline_uuid, player["name"]]
                    elif self.__mode == 'online' and offline_uuid not in self.__player_map:
                        self.__player_map[offline_uuid] = [online_uuid, player["name"]]
                else:
                    print(f'[{file_name["name"]}] {player["name"]} could not be found as a premium username')
            return self.__player_map
        except Exception as e:
            print(f'[{file_name["name"]}] ERROR could not load file for getting information')
            logging.exception(e)
