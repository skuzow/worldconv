import hashlib
import logging
import time
import requests

from json import JSONDecodeError
from worldconv.utils import logger


MOJANG_API: str = 'https://api.mojang.com/users/profiles/minecraft'


def generate_online(username: str, check: bool) -> str | bool:
    # gets online uuid via mojang api
    while True:
        try:
            online_uuid: str | bool = __add_stripes(__online_uuid(username))
            logger.info(f'''[online] username: {username}
                         -> uuid: {online_uuid}''')
            time.sleep(0.5)
            break
        except JSONDecodeError:
            online_uuid = False
            break
        except Exception as e:
            if check:
                logging.exception(e)
                online_uuid = False
                break
            else:
                logger.warning(f'''Mojang api not working properly for
                                {username}, will try again in 5s''')
                time.sleep(5)
    return online_uuid


def generate_offline(username: str) -> str:
    # extracted from the java code:
    # new GameProfile(UUID.nameUUIDFromBytes(("OfflinePlayer:" + name)
    #       .getBytes(Charsets.UTF_8)), name));
    string: str = "OfflinePlayer:" + username
    hash: bytes = hashlib.md5(string.encode('utf-8')).digest()
    byte_array: list[int] = [byte for byte in hash]
    byte_array[6] = hash[6] & 0x0f | 0x30
    byte_array[8] = hash[8] & 0x3f | 0x80
    offline_uuid = __add_stripes(bytes(byte_array).hex())
    logger.info(f'[offline] username: {username} -> uuid: {offline_uuid}')
    return offline_uuid


def __online_uuid(username: str) -> str:
    return requests.get(f'{MOJANG_API}/{username}?').json()["id"]


def __add_stripes(uuid: str) -> str:
    return f'''{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}
            -{uuid[16:20]}-{uuid[20:]}'''
