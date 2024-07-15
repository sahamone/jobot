import json



### CONFIG.PY ###
# This file is used to read the config.json file and return the data as a dictionary.
#################

__config = None

def get_config():
    global __config
    if __config == None :
        with open('config.json') as f:
            __config = json.load(f)


    return __config


# END OF FILE