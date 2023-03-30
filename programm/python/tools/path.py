import os

def realcd(path: str):
    '''
    Set's pwd to @param path
    '''
    os.chdir(os.path.abspath(path) if os.path.exists(path) else os.path.defpath)

