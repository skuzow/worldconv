import json
import logging
import os

from uuidworldconverter.utils import logger


class Modify:

    def __init__(self, config, player_map):
        self.__config = config
        self.__uuid_map = player_map

    def modify_json(self, file):
        # if file_name change it's deactivated via config, it exits
        if not file["enable"]:
            return print(f'[{logger.INFO}] [{file["name"]}] Skipped, {file["name"]}: {file["enable"]}')
        file_path = os.path.join(os.getcwd(), self.__config["server_directory"], file["name"])
        # if file doesn't exist, returns with error print
        if not os.path.isfile(file_path):
            return print(f'[{logger.WARNING}] [{file["name"]}] File not found in directory: {file_path}')
        # open, loads & closes file_name in read mode
        read_file = open(file_path, 'r')
        file_json = json.load(read_file)
        read_file.close()
        # for each in file_json
        print(f'[{logger.INFO}] [{file["name"]}] Starting changing file: {file_path}')
        file_change = False
        for player in file_json:
            if player["uuid"] in self.__uuid_map:
                print(
                    f'[{logger.INFO}] [{file["name"]}] {self.__uuid_map[player["uuid"]][1]} : {player["uuid"]} -> {self.__uuid_map[player["uuid"]][0]}')
                player["uuid"] = self.__uuid_map[player["uuid"]][0]
                file_change = True
        # if something was changed
        if file_change:
            try:
                # opens file_name in write mode
                write_file = open(file_path, 'w')
                # save changes into the file in the disk, then closes it
                json.dump(file_json, write_file, indent=4)
                print(f'[{logger.INFO}] [{file["name"]}] Successfully written json to file: {file_path}')
                write_file.close()
            except Exception as e:
                print(f'[{logger.ERROR}] [{file["name"]}] Could not dump json: {file_path}')
                logging.exception(e)
        else:
            print(f'[{logger.WARNING}] [{file["name"]}] Nothing changed so file stays same: {file_path}')

    def modify_folder(self, folder):
        # if folder change it's deactivated via config it exits
        if not folder["enable"]:
            return print(f'[{logger.INFO}] [{folder["name"]}] Skipped, {folder["name"]}: {folder["enable"]}')
        folder_path = os.path.join(os.getcwd(), self.__config["server_directory"], self.__config["world_directory"],
                                   folder["name"])
        # if folder doesn't exist, returns with error print
        if not os.path.isdir(folder_path):
            return print(f'[{logger.ERROR}] [{folder["name"]}] Directory not found: {folder_path}')
        # for each in folder_path
        print(f'[{logger.INFO}] [{folder["name"]}] Starting changing folder files: {folder_path}')
        file_change = False
        for file in os.listdir(folder_path):
            file_split = str(file).split(".")
            file_uuid = file_split[0]
            if file_uuid in self.__uuid_map:
                old_name = os.path.abspath(os.path.join(folder_path, file))
                new_name = os.path.abspath(
                    os.path.join(folder_path, f'{self.__uuid_map[file_uuid][0]}.{file_split[1]}'))
                try:
                    # changes file_name
                    os.rename(old_name, new_name)
                    file_change = True
                    print(f'[{logger.INFO}] [{folder["name"]}] {self.__uuid_map[file_uuid][1]} : {file} -> {self.__uuid_map[file_uuid][0]}.{file_split[1]}')
                    print(f'[{logger.INFO}] [{folder["name"]}] oldpath: {old_name}')
                    print(f'[{logger.INFO}] [{folder["name"]}] newpath: {new_name}')
                except Exception as e:
                    logging.exception(e)
                    print(f'[{logger.ERROR}] [{folder["name"]}] Could not rename file: {file}')
        if not file_change:
            print(f'[{logger.WARNING}] [{folder["name"]}] Nothing changed so folder stays same: {folder_path}')
