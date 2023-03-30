from ..core import config
from . import wrap
from ..tools import functions
from ..locale import locale, tokens

def _default_vars(vars: dict):
    dict_keys = []
    newdict = {}
    for x in vars.keys():
        dict_keys.append(x.lower())
        newdict[x.lower()] = vars[x]
    if "ps1" in dict_keys:
        return newdict["ps1"]
    else:
        return ""


def command_processor(args: list):
    '''
    Continuous of __main__.main().
    Processing commands.
    '''
    commands = wrap.get_commands_ff(args[0]) if len(args) > 0 else []
    variables = {} 
    in_command = len(commands) != 0
    i = 0
    while True:
        PS1 = _default_vars(variables)    
        if not in_command:
            try:
                command = input(PS1)
            except:
                command = "exit"
        else:
            command = commands[i]
        args = wrap.execute(command, vars=variables)
        syscode = args if type(args) == int else args[0]
        if type(args) != int and len(args) > 1:
            other = args[1:]
        if syscode == config.SYSEXIT and not in_command:
            break
        elif syscode == config.GLOBEXIT: # it terminate work anywhere :)
            break
        elif syscode == config.EXPORTVAR:
            try:
                variables[other[0]] = other[1]
            except Exception as e:
                functions.info(f"Can't set variable! {e}", level='e')
        else:
            functions.info(f"{locale.get_by_token(tokens.ERRROR_SYSCODE_UNREGISTERED)} {syscode}", level='e')
        
        if len(commands) - 1 != i:
            i += 1
        else:
            in_command = False