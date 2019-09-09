import yaml
from os.path import isfile, exists
# perhaps rename to parse_config???
def get_config(default_file = 'config.yml'):
    exists = isfile('../config.yml')
    if exists:
        config_file = '../config.yml'
        # Store configuration file values
    else:
        # Keep presets
        config_file = default_file
    with open(config_file, 'r') as ymlfile:
        # Latest version
        if hasattr(yaml, 'FullLoader'):
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        # PyYaml 3.
        else:
            cfg = yaml.load(ymlfile)
    return cfg