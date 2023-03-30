from ..core import config
from ..tools import functions
from ..locale import locale, tokens
from . import commands
import os

def get_commands_ff(_path: str, pwd=".") -> list:
    '''
    Gets command list from file
    '''
    path = os.path.join(os.path.abspath(pwd), _path) if not os.path.isabs(_path) else _path
    commands = None
    if not os.path.exists(path):
        functions.info(f"{locale.get_by_token(tokens.PATH_NOT_EXISTS)} {_path}")
        return []
    if not os.path.isfile(os.path.realpath(path)):
        functions.info(f"{locale.get_by_token(tokens.NOT_A_FILE)} {_path}")
        return []
    functions.info(f"{locale.get_by_token(tokens.FILE_OPEN_TRY)}")
    functions.info(f"{locale.get_by_token(tokens.FILE_NAME_DISPLAY)} {_path}", level='d')
    try:
        file = open(path, "r")
        commands = file.readlines()
        file.close()
    except Exception as e:
        functions.info(f"{locale.get_by_token(tokens.ERROR_FILE_READ)} {e}", level='e')
    return commands if not commands == None else []

def execute(command: str, vars: dict={}) -> int:
    '''
    Execute command
    '''
    if len(command) == 0:
        return config.CONTINUE
    _cmd = command.strip().split()
    _self_cmd = _cmd[0].lower().strip()
    _cmd_args = []
    _vars_keys = []
    for x in vars.keys():
        _vars_keys.append(x)
    if len(_cmd) > 1:
        _temp = _cmd[1:]
        for x in range(len(_temp)):
            if _temp[x].startswith("$"):
                if _temp[x].lstrip("$") in _vars_keys:
                    _cmd_args.append(vars[_temp[x].lstrip("$")])
                else:
                    _cmd_args.append(" ")
            else:
                _cmd_args.append(_temp[x])
    if _self_cmd == 'quit' or _self_cmd == 'exit':
        return config.SYSEXIT
    elif _self_cmd == 'globexit':
        return config.GLOBEXIT
    elif _self_cmd == 'pause':
        commands.pause()
        return config.CONTINUE
    elif _self_cmd == "lcls":
        commands.lcls(_cmd_args)
        return config.CONTINUE
    elif _self_cmd == 'export':
        variable, value = commands.export(_cmd_args)
        return config.EXPORTVAR, variable, value
    elif _self_cmd == 'cd':
        commands.cd(_cmd_args)
        return config.CONTINUE
    elif _self_cmd == 'read': # Read and save variable: read <variable> <text>
        variable, value = commands.read(_cmd_args)
        return config.EXPORTVAR, variable, value
    elif _self_cmd == 'echo':
        commands.echo(_cmd_args)
        return config.CONTINUE
    elif _self_cmd == 'loadcmd':
        file = commands.loadcmd() if commands.BASE_IMPORTED else None
        return config.LOADFILE
    else:
        return config.NOCOMMAND
