from configparser import ConfigParser
import os
import shutil
#'\033[91m'=Red
#'\033[0m'=White
#'\033[92m'=green
 
config = ConfigParser()

def DeleteFile(Function: str, y: os.DirEntry[str]):
    try:
        if config[Function]['askBeforeDelete'] == 'False': response = 'Y'
        else: response = input(f"\033[0mAre you sure you want to delete {y.name}? [y/N] ").capitalize()
    except: response = input(f"\033[0mAre you sure you want to delete {y.name}? [y/N] ").capitalize()

    match response:
        case 'Y':
            try:
                if (y.is_file()):os.remove(y.path)
                elif (y.is_dir):shutil.rmtree(y.path)
                if os.path.exists(y.path) == False: print(f"\033[92m[OK] {y.name} Deleted Correctly")
            except Exception as err: print(f"\033[91m[ERR] Couldn't delete {y.path} {err}") 

def Move(y: os.DirEntry[str], finalPath, fun: str):
    if os.path.isdir(finalPath):
        print('\033[0m' + "moving " + y.name + " to " + finalPath +"...")
        try:
            shutil.move(y.path, finalPath)
            print('\033[92m' + "[OK] Done")
        except Exception as err:
            print(f"\033[91m[Err] Can't move files {err}")
    elif finalPath == "Delete":
        DeleteFile(fun, y)

                                        

def Main():
    config.read("config.conf")
  

    for x in config:

        paths: list = []
        if x != "DEFAULT": 
            try: paths.extend(config[x]['paths'].split(','))
            except Exception as err: print(f"\033[91m[Err] option 'paths' not found in {x}")

            for i in paths:
                currentpath: str = i 
                if   os.path.isdir(currentpath):
                    print('\033[92m' + "scanning " + currentpath)
                else:
                    print('\033[93m' + f"[Err] {currentpath} isn't a valid directory")
                    continue
                
                mode = config[x]['mode']
                match mode:
                            case "byExtension":
                                for ext in config[x]:
                                    if ext != 'mode' and ext != 'paths':
                                        finalPath: str = "".join(config[x][ext])
                                        for y in os.scandir(currentpath):
                                            if y.path.endswith(ext): Move(y, finalPath, x)
                                            elif ext == 'dir' and y.is_dir(): Move(y, finalPath, x)

                                                
                            case "Clear":
                                files = os.scandir(currentpath)
                                for y in files:
                                    DeleteFile(currentpath, y)

                            case "byName":
                                for file in config[x]:
                                    if file != 'mode' and file != 'paths':
                                        finalPath: str = "".join(config[x][file])
                                        for y in os.scandir(currentpath):
                                            if y.name == file:
                                                Move(y, finalPath, x)

                            case _:
                                print('\033[91m' + "[err]" + '"' + "mode = " + mode + '"' + " is not a valid configuration")
                                continue
                
if os.path.isfile('./config.conf'):
    print('\033[92m' + "[OK] Config file found")
    Main()
else:
    print('\033[91m'+"[Err] No Config File!!")
    try: 
        print("Creating Config file...")
        shutil.copyfile('Exemple.conf', 'config.conf')
        if os.path.isfile('./config.conf') : 
            print('\033[92m' + "[OK] Done")
            input("Config file created correctly, now go configure it!! (enter to exit)")
            exit(0)
    except Exception as err: 
        input(f"\033[91m[CRITICAL ERROR!!] Can't create config file {err} (Enter To Exit)")
        exit(0)