from ...tools import functions, path
from ...locale import locale, tokens

import os

def lcls(args: list) -> None:
    if len(args) > 0:
        if os.path.exists(args[-1]):
            dir = args[-1]
        else:
            functions.info(f"{locale.get_by_token(tokens.PATH_NOT_EXISTS)} {dir}", level="e")
            return
    else:
        dir = "."
    content = os.listdir(dir)
    part = len(content) % 5
    for x in range((len(content) - part) // 5):
        print(" ".join(content[5*x:5*(x+1)])+"\n")
    if part != 0:
        print(" ".join(content[-part:])+"\n")

def export(args: list) -> tuple[str, str]:
    '''
    Exports variable
    @return variable - Variable
    @return value - Value of
    Works as bash's export
    '''
    
    pass

def cd(args: list) -> None:
    '''
    Cd to @param args[-1]
    '''
    if len(args) > 0:
        if os.path.exists(args[-1]):
            if os.path.isdir(args[-1]):
                dir = args[-1]
            else:
                functions.info(f"{locale.get_by_token(tokens.NOT_A_DIR)} {args[-1]}", level='e')
                return
        else:
            functions.info(f"{locale.get_by_token(tokens.PATH_NOT_EXISTS)} {args[-1]}")
            return
    else:
        dir = os.path.defpath
    path.realcd(dir)
