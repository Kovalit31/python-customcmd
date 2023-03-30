from ..core import config
from ..tools import functions
from ..locale import locale, tokens
from . import commands
import os

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
        file = commands.loadcmd(_cmd_args)
        return config.LOADFILE, file
    else:
        return config.NOCOMMAND
