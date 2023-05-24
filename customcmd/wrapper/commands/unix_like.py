import os
import pathlib
import copy
from customcmd.tools import global_functions, pathutil

def ls(args: list) -> None:
    '''
    Lists current directory in local system (without arguments)
    '''
    args = args[1:]
    if len(args) > 0:
        dir = os.fspath(pathutil.get_full_path(args[0]))
    else:
        dir = "."
    if dir == None:
        return
    remapped = [[] for _ in range(5)]
    _biggest1 = 0
    _biggest2 = 0
    content = os.listdir(dir) if not os.path.isfile(dir) else [dir]
    for x in range(len(content)):
        start, end = global_functions.char_count(content[x], " ")
        if end - start >= 0 and start + end != -2:
            content[x] = "\"" + content[x] + "\""
        if not x in range(5):
            _biggest2 = len(content[x]) if len(content[x]) > _biggest2 else _biggest2
            content[x] = " "*(_biggest1-len(remapped[x%5][-1].strip()))+content[x]
        else:
            _biggest1 = len(content[x]) if len(content[x]) > _biggest1 else _biggest1
        if x % 5 == 4:
            _biggest1 = copy.copy(_biggest2) + 1 if not x in range(5) else _biggest1 + 1
            _biggest2 = 0
        remapped[x%5].append(content[x])
    for x in range(len(remapped)):
        print(" ".join(remapped[x]))
    
def cd(args: list) -> None:
    '''
    Cd to @param args[-1]
    '''
    args = args[1:]
    if len(args) > 0:
        path = pathutil.is_dir_throw(args[0])
        if path == None:
            return
    else:
        path = os.fspath(pathlib.Path.home())
    os.chdir(path if os.path.exists(path) else os.fspath(pathlib.Path(".").absolute()))

def echo(args: list) -> None:
    '''
    Echo all in @param args
    '''
    args = args[1:]
    joined_args = " ".join(args)
    start, end = global_functions.char_count(joined_args, '"')
    print(joined_args.replace('"', "", (end - start) - (end - start) % 2))

def pwd(_: list, _return_path=False) -> None:
    '''
    Prints current path
    '''
    path = os.path.abspath(os.path.curdir)
    if _return_path:
        return path
    print(path)
