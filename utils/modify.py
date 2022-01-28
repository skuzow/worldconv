import json
import os


def modifyjson(filename, config, playermap):
    prompt = f'[{filename}]'
    # if filename change it's deactivated via config it exits
    if not config[f'change_{filename[:-5]}']:
        return print(f'{prompt} Skipped, change_whitelist: {config[f"change_{filename[:-5]}"]}')
    # open, loads & closes file
    filepath = os.path.join(config['server_directory'], filename)
    # if file doesn't exist, returns with error print
    if not os.path.isfile(filepath):
        return print(f'{prompt} ERROR File Not Found in directory: {filepath}')
    # open, loads & closes filename in read mode
    readfile = open(filepath, 'r')
    filejson = json.load(readfile)
    filechange = False
    readfile.close()
    # for each in filejson
    print(f'{prompt} Starting changing file: {filepath}')
    for player in filejson:
        if player['uuid'] in playermap:
            print(f'{prompt} {playermap[player["uuid"]][1]} : {player["uuid"]} -> {playermap[player["uuid"]][0]}')
            player['uuid'] = playermap[player['uuid']][0]
            filechange = True
    # if something was changed
    if filechange:
        # open filename in write mode
        writefile = open(filepath, 'w')
        # save changes into the file in the disk, then closes it
        json.dump(filejson, writefile, indent=4)
        writefile.close()
        print(f'{prompt} Successfully written json to file: {filepath}')
    else:
        print(f'{prompt} Nothing changed so file stays same: {filepath}')
