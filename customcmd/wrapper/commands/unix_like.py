import os
from customcmd.tools import global_functions, pathutil

def ls(args: list) -> None:
    '''
    Lists current directory in local system
    '''
    args = args[1:]
    print(args)
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
    args = args[1:]
    if len(args) > 0:
        path = pathutil.is_dir_throw(args[-1])
        if path == None:
            return
    else:
        path = os.path.defpath
    os.chdir(os.path.abspath(path) if os.path.exists(path) else os.path.defpath)

def echo(args: list) -> None:
    '''
    Echo all in @param args
    '''
    args = args[1:]
    joined_args = " ".join(args)
    quote_count = global_functions.char_count(joined_args, '"')
    print(joined_args.replace('"', "", quote_count - quote_count % 2))

def pwd(_: list, _return_path=False) -> None:
    '''
    Prints current path
    '''
    path = os.path.abspath(os.path.curdir)
    if _return_path:
        return path
    print(path)
