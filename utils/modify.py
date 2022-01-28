import json
import os


def modifyjson(filename, config, playermap):
    prompt = f'[{filename}]'
    # if filename change it's deactivated via config it exits
    if not config[f'change_{filename[:-5]}']:
        return print(f'{prompt} Skipped, change_{filename[:-5]}: {config[f"change_{filename[:-5]}"]}')
    filepath = os.path.join(config['server_directory'], filename)
    # if file doesn't exist, returns with error print
    if not os.path.isfile(filepath):
        return print(f'{prompt} ERROR file not found in directory: {filepath}')
    # open, loads & closes filename in read mode
    readfile = open(filepath, 'r')
    filejson = json.load(readfile)
    readfile.close()
    # for each in filejson
    print(f'{prompt} Starting changing file: {filepath}')
    filechange = False
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


def modifyfolder(folder, config, playermap):
    prompt = f'[{folder}]'
    # if folder change it's deactivated via config it exits
    if not config[f'change_{folder}']:
        return print(f'{prompt} Skipped, change_{folder}: {config[f"change_{folder}"]}')
    folderpath = os.path.join(config['server_directory'], config['world_directory'], folder)
    # if folder doesn't exist, returns with error print
    if not os.path.isdir(folderpath):
        return print(f'{prompt} ERROR not found directory: {folderpath}')
    # for each in folderpath
    print(f'{prompt} Starting changing folder files: {folderpath}')
    filechange = False
    for filename in os.listdir(folderpath):
        filesplit = str(filename).split(".")
        fileuuid = filesplit[0]
        if fileuuid in playermap:
            oldname = os.path.abspath(os.path.join(folderpath, filename))
            newname = os.path.abspath(os.path.join(folderpath, f'{playermap[fileuuid][0]}.{filesplit[1]}'))
            try:
                os.rename(oldname, newname)
                filechange = True
                print(f'{prompt} {playermap[fileuuid][1]} : {filename} -> {playermap[fileuuid][0]}.{filesplit[1]}')
                print(f'{prompt} oldpath: {oldname}')
                print(f'{prompt} newpath: {newname}')
            except:
                print(f'{prompt} ERROR could not rename file: {filename}')
    if not filechange:
        print(f'{prompt} Nothing changed so folder stays same: {folderpath}')
