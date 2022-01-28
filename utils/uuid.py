import hashlib
import requests


def getonlineuuid(username):
    onlineuuid = addstripes(requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}?').json()['id'])
    print(f'[online] username: {username} -> uuid: {onlineuuid}')
    return onlineuuid


def getofflineuuid(username):
    # extracted from the java code:
    # new GameProfile(UUID.nameUUIDFromBytes(("OfflinePlayer:" + name).getBytes(Charsets.UTF_8)), name));
    string = "OfflinePlayer:" + username
    hash = hashlib.md5(string.encode('utf-8')).digest()
    byte_array = [byte for byte in hash]
    byte_array[6] = hash[6] & 0x0f | 0x30
    byte_array[8] = hash[8] & 0x3f | 0x80
    offlineuuid = addstripes(bytes(byte_array).hex())
    print(f'[offline] username: {username} -> uuid: {offlineuuid}')
    return offlineuuid


def addstripes(string):
    return string[:8] + '-' + string[8:12] + '-' + string[12:16] + '-' + string[16:20] + '-' + string[20:]
