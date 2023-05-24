import os
from . import global_functions
from ..locale import locale

# ===================
#  Path constructors
# ===================

def get_full_path(_path: str, return_else=False):
    '''
    Get full path to file or dir
    '''
    path = os.path.join(os.path.abspath("."), _path) if not os.path.isabs(_path) else _path
    if os.path.exists(path) or return_else:
        return os.path.realpath(path)
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
    if os.path.isfile(path):
        return path
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
    if os.path.isdir(path):
        return path
    else:
        global_functions.out(f"{locale.get_by_token('io.path.error.notdir').format(path=_path)}", level='e')
        return None
