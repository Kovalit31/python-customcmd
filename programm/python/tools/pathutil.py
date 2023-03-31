import os
from . import functions
from ..locale import locale, tokens

def realcd(path: str):
    '''
    Set's pwd to @param path
    '''
    os.chdir(os.path.abspath(path) if os.path.exists(path) else os.path.defpath)

def get_full_path(_path: str, return_else=False):
    '''
    Get full path to file or dir
    '''
    path = os.path.join(os.path.abspath("."), _path) if not os.path.isabs(_path) else _path
    if os.path.exists(path) or return_else:
        return os.path.realpath(path)
    else:
        functions.info(f"{locale.get_by_token(tokens.PATH_NOT_EXISTS)} {_path}")
        return None
    
def is_file_throw(_path: str):
    '''
    Checks and get out, if path is file, else returns None
    '''
    path = get_full_path(_path)
    if path == None:
        return None
    if os.path.isfile(path):
        return path
    else:
        functions.info(f"{locale.get_by_token(tokens.NOT_A_FILE)} {_path}", level='e')
        return None
    
def is_dir_throw(_path: str):
    '''
    Checks and get out, if path is dir, else returns None
    '''
    path = get_full_path(_path)
    if path == None:
        return None
    if os.path.isdir(path):
        return path
    else:
        functions.info(f"{locale.get_by_token(tokens.NOT_A_DIR)} {_path}", level='e')
        return None
    