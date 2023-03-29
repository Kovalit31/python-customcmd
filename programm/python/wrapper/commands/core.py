from ...tools import functions
from ...locale import locale, tokens

import os

def lcls(args: list) -> None:
    if len(args) > 0:
        if os.path.exists(args[-1]):
            dir = args[-1]
        else:
            functions.info(f"{locale.get_by_token()}", level="e")
            return
    else:
        dir = "."
    content = os.listdir(dir)
    part = len(content) % 5
    for x in range((len(content) - part) // 5):
        print(" ".join(content[5*x:5*(x+1)])+"\n")
    if part != 0:
        print(" ".join(content[-part:])+"\n")

def export(args: list) -> tuple(str, str):
    '''
    Exports variable
    @return variable - Variable
    @return value - Value of
    Works as bash's export
    '''
    
    pass