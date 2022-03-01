import hashlib
import logging
import time
import requests
# import re

from json import JSONDecodeError
from uuidworldconverter.utils import logger


""" mojang removed it :(
def check_mojang_api():
    return True if requests.get(f'https://status.mojang.com/check').json()[5]["api.mojang.com"] == 'green' else False
"""


def generate_online(username):
    # gets online uuid via mojang api
    try:
        online_uuid = __add_stripes(requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}?').json()["id"])
        print(f'[{logger.INFO}] [online] username: {username} -> uuid: {online_uuid}')
        time.sleep(0.5)
    except JSONDecodeError:
        online_uuid = False
    except Exception as e:
        online_uuid = False
        logging.exception(e)
    return online_uuid


def generate_offline(username):
    # extracted from the java code:
    # new GameProfile(UUID.nameUUIDFromBytes(("OfflinePlayer:" + name).getBytes(Charsets.UTF_8)), name));
    string = "OfflinePlayer:" + username
    hash = hashlib.md5(string.encode('utf-8')).digest()
    byte_array = [byte for byte in hash]
    byte_array[6] = hash[6] & 0x0f | 0x30
    byte_array[8] = hash[8] & 0x3f | 0x80
    offline_uuid = __add_stripes(bytes(byte_array).hex())
    print(f'[{logger.INFO}] [offline] username: {username} -> uuid: {offline_uuid}')
    return offline_uuid


"""
def generate_player_name(uuid):
    # removes stripes
    proper_uuid = re.sub('[-]', '', uuid)
    # tries to get player name via mojang api
    try:
        name = requests.get(f'https://api.mojang.com/user/profiles/{proper_uuid}/names').json()[0]["name"]
    except JSONDecodeError:
        name = False
    except Exception as e:
        name = False
        logging.exception(e)
    return name
"""


def __add_stripes(uuid):
    return uuid[:8] + '-' + uuid[8:12] + '-' + uuid[12:16] + '-' + uuid[16:20] + '-' + uuid[20:]
