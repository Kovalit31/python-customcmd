from ...tools import functions, path
from ...locale import locale, tokens

import os

def lcls(args: list) -> None:
    '''
    Lists current directory in local system
    '''
    if len(args) > 0:
        if os.path.exists(args[-1]):
            dir = args[-1]
        else:
            functions.info(f"{locale.get_by_token(tokens.PATH_NOT_EXISTS)} {args[-1]}", level="e")
            return
    else:
        dir = "."
    content = os.listdir(dir) if not os.path.isfile(dir) else [dir]
    part = len(content) % 5
    for x in range((len(content) - part) // 5):
        print(" ".join(content[5*x:5*(x+1)]))
    if part != 0:
        print(" ".join(content[-part:]))

def export(args: list) -> tuple[str, str]:
    '''
    Exports variable
    @return variable - Variable
    @return value - Value of
    Works as bash's export
    '''
    args_remapped = []
    found = False
    for x in range(len(args)):
        if "=" in args[x] and not found:
            parts = args[x].split("=", 1)
            var, val = parts[0], parts[1]
            args_remapped.append(var)
            args_remapped.append("=")
            args_remapped.append(val)
            found = not found
        else:
            args_remapped.append(args[x])
    _variable = []
    _value = []
    is_got = False
    for x in range(len(args_remapped)):
        if args_remapped[x] == "" and x != len(args_remapped) - 1:
            continue
        if not is_got:
            if args_remapped[x] == "=":
                is_got = not is_got
                continue
            _variable.append(args_remapped[x])
        else:
            _value.append(args_remapped[x])       
    var = "_".join(_variable)
    val = " ".join(_value)
    quote_count = functions.char_count(val, '"')
    val = val.replace('"', '', quote_count - quote_count % 2)
    return var, val
            
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

def pause() -> None:
    '''
    Pause programm and wait user
    '''
    input(locale.get_by_token(tokens.COMMAND_PAUSE_TITLE))

def echo(args: list) -> None:
    '''
    Echo all in @param args
    '''
    joined_args = " ".join(args)
    quote_count = functions.char_count(joined_args, '"')
    print(joined_args.replace('"', "", quote_count - quote_count % 2))
    
def read(args: list) -> tuple[str, str]:
    '''
    Reads standart input to get value of variable
    '''
    if not len(args) > 0:
        functions.info(f"{locale.get_by_token(tokens.FEW_ARGS_FOR_READ)}")
        return None, None
    inputted = input(args[1] if len(args) > 1 else "")
    return args[0], inputted