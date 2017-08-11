import os
import anyconfig

def config_loader():
    if os.path.isfile('./config/production.yml'):
        load_file = './config/production.yml'
    elif os.path.isfile('./config/development.yml'):
        load_file = './config/development.yml'
    else:
        load_file = './config/default.yml'

    return anyconfig.load(load_file)
