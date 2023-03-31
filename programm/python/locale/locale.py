import os

from ..core import config
from ..tools import functions

PATH = os.path.join(os.path.dirname(__file__), "lang")

def get_by_token(token: str, lang=config.DEFAULT_LANG) -> str:
    '''
    Gets language value with token
    '''
    try:
        file = open(os.path.join(PATH, f"{lang}.po"), "r", encoding="utf-8")
        data = file.readlines()
        file.close()
    except Exception as e:
        functions.info(f"Can't get locale! {e}", level='f')
        return
    for x in range(len(data)):
        if data[x].strip() == token.lower().strip():
            try:
                return data[x+1].strip()
            except Exception as e:
                functions.info(f"Developer! File {f'{lang}.po'} not fully edited!", level="d")
                return f"{{{token}}}"
    else:
        functions.info(f"Developer! File {f'{lang}.po'} doesn't content {token}!", level='d')
        return f"{{{token}}}"
        