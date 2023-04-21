import os
from ...tools import functions, pathutil

def ls(args: list) -> None:
    '''
    Lists current directory in local system
    '''
    if len(args) > 0:
        dir = pathutil.get_full_path(args[0])
    else:
        dir = "."
    if dir == None:
        return
    content = os.listdir(dir) if not os.path.isfile(dir) else [dir]
    part = len(content) % 5
    for x in range((len(content) - part) // 5):
        print(" ".join(content[5*x:5*(x+1)]))
    if part != 0:
        print(" ".join(content[-part:]))
    
def cd(args: list) -> None:
    '''
    Cd to @param args[-1]
    '''
    if len(args) > 0:
        dir = pathutil.is_dir_throw(args[-1])
        if dir == None:
            return
    else:
        dir = os.path.defpath
    pathutil.realcd(dir)

def echo(args: list) -> None:
    '''
    Echo all in @param args
    '''
    joined_args = " ".join(args)
    quote_count = functions.char_count(joined_args, '"')
    print(joined_args.replace('"', "", quote_count - quote_count % 2))

def exit(args: list) -> None:
    '''
    It's do nothing!
    '''
    pass

def pwd(args: list) -> None:
    '''
    Prints current path
    '''
    print(os.path.abspath(os.path.curdir))
