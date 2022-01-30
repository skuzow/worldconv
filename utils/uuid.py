import hashlib
import requests


class Uuid:

    def generate_online(self, username: str):
        online_uuid = self.__add_stripes(requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}?').json()['id'])
        print(f'[online] username: {username} -> uuid: {online_uuid}')
        return online_uuid

    def generate_offline(self, username: str):
        # extracted from the java code:
        # new GameProfile(UUID.nameUUIDFromBytes(("OfflinePlayer:" + name).getBytes(Charsets.UTF_8)), name));
        string = "OfflinePlayer:" + username
        hash = hashlib.md5(string.encode('utf-8')).digest()
        byte_array = [byte for byte in hash]
        byte_array[6] = hash[6] & 0x0f | 0x30
        byte_array[8] = hash[8] & 0x3f | 0x80
        offline_uuid = self.__add_stripes(bytes(byte_array).hex())
        print(f'[offline] username: {username} -> uuid: {offline_uuid}')
        return offline_uuid

    def __add_stripes(self, uuid):
        return uuid[:8] + '-' + uuid[8:12] + '-' + uuid[12:16] + '-' + uuid[16:20] + '-' + uuid[20:]
