from sys import platform

def get_env():
    if platform in [None, 'linux']:
        return "production"
    else:
        return "dev"