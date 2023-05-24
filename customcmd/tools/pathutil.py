import os
import pathlib
from . import global_functions
from ..locale import locale

# ===================
#  Path constructors
# ===================

def get_full_path(_path: str, return_else=False):
    '''
    Get full path to file or dir
    '''
    path = pathlib.Path(_path).expanduser()
    if path.exists() or return_else:
        return path.resolve()
    else:
        global_functions.out(f"{locale.get_by_token('io.path.error.notexists').format(path=_path)}")
        return None
    
# ===================
#    Type checker
# ===================

def is_file_throw(_path: str):
    '''
    Checks and get out, if path is file, else returns None
    '''
    path = get_full_path(_path)
    if path == None:
        return None
    if path.is_file():
        return os.fspath(path)
    else:
        global_functions.out(f"{locale.get_by_token('io.path.error.notfile').format(path=_path)}", level='e')
        return None
    
def is_dir_throw(_path: str):
    '''
    Checks and get out, if path is dir, else returns None
    '''
    path = get_full_path(_path)
    if path == None:
        return None
    if path.is_dir():
        return os.fspath(path)
    else:
        global_functions.out(f"{locale.get_by_token('io.path.error.notdir').format(path=_path)}", level='e')
        return None
