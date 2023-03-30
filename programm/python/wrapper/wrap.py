from ..core import config
from ..tools import functions
from ..locale import locale, tokens
from . import commands
import os

def get_commands_ff(_path: str, pwd=".") -> list:
    '''
    Gets command list from file
    '''
    path = os.path.join(os.path.abspath(pwd), _path) if os.path.isabs(_path) else _path
    commands = None
    functions.info("Trying to process file")
    functions.info(f"File: {path}", level='d')
    try:
        file = open(path, "r")
        commands = file.readlines()
        file.close()
    except Exception as e:
        functions.info(f"{locale.get_by_token(tokens.ERROR_FILE_READ)} {e}", level='e')
    return commands if not commands == None else []




def execute(command: str, vars={}) -> int:
    '''
    Execute command
    '''
    _cmd = command.lower().strip().split()
    _self_cmd = _cmd[0].strip()
    if _self_cmd == 'quit' or _self_cmd == 'exit':
        return config.SYSEXIT
    elif _self_cmd == 'globexit':
        return config.GLOBEXIT
    elif _self_cmd == 'pause':
        input(locale.get_by_token(tokens.COMMAND_PAUSE_TITLE))
        return config.CONTINUE
    elif _self_cmd == "lcls":
        commands.lcls(_cmd[1:])
        return config.CONTINUE
    elif _self_cmd == 'export':
        variable, value = commands.export(_cmd[1:])
        return config.EXPORTVAR, variable, value
    else:
        return config.NOCOMMAND
