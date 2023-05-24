from . import config

def get_version() -> str:
    return str(config.MAJOR_VER)+str(config.MINOR_VER)+str(config.PATCH_VER)+"-"+config.RELEASE_VER+"-"+config.SALT

