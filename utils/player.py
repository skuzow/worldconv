import json
import os

from utils.uuid import getofflineuuid, getonlineuuid


def getplayermap(config, mode):
    # whitelist
    whitelistpath = os.path.join(config['server_directory'], 'whitelist.json')
    # map -> searchuuid : [ changeuuid, playername ]
    playermap = {}
    # checks if whitelist.json exists, if it doesn't it exits with playermap.__sizeof__() = 0
    if not os.path.isfile(whitelistpath):
        return playermap
    # open, loads & closes whitelist.json in read mode
    whitelistfile = open(whitelistpath, 'r')
    whitelist = json.load(whitelistfile)
    whitelistfile.close()
    # for each in whitelist.json
    for player in whitelist:
        try:
            offlineuuid = getofflineuuid(player['name'])
            onlineuuid = getonlineuuid(player['name'])
            if mode == 'offline':
                playermap[onlineuuid] = [offlineuuid, player['name']]
            elif mode == 'online':
                playermap[offlineuuid] = [onlineuuid, player['name']]
        except:
            print('[whitelist.json] {} could not be found as a premium username'.format(player['name']))
    # ops
    checkfile('ops.json', config, mode, playermap)
    # banned-players
    checkfile('banned-players.json', config, mode, playermap)
    # prints "pretty" playermap
    print('[playermap] {}'.format(json.dumps(playermap, indent=4)))
    return playermap


def checkfile(filename, config, mode, uuidmap):
    filepath = os.path.join(config['server_directory'], filename)
    if os.path.isfile(filepath):
        # open, loads & closes filename in read mode
        file = open(filepath, 'r')
        filejson = json.load(file)
        file.close()
        # for each in filejson
        for player in filejson:
            try:
                if mode == 'offline':
                    onlineuuid = getonlineuuid(player['name'])
                    if onlineuuid not in uuidmap:
                        uuidmap[onlineuuid] = [getofflineuuid(player['name']), player['name']]
                elif mode == 'online':
                    offlineuuid = getofflineuuid(player['name'])
                    if offlineuuid not in uuidmap:
                        uuidmap[offlineuuid] = [getonlineuuid(player['name']), player['name']]
            except:
                print(f'[{filename}] {player["name"]} could not be found as a premium username')
