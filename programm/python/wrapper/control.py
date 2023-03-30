from ..core import config
from . import wrap
from ..tools import functions
from ..locale import locale, tokens

def _default_vars(vars: dict):
    '''
    Return default vars for @function command_processor
    '''
    dict_keys = []
    newdict = {}
    for x in vars.keys():
        dict_keys.append(x.lower())
        newdict[x.lower()] = vars[x]
    PS1 = newdict["ps1"] if "ps1" in dict_keys else ''
    CONST_LANG = config.DEFAULT_LANG
    return PS1, CONST_LANG

def command_processor(args: list):
    '''
    Continuous of __main__.main().
    Processing commands.
    '''
    _commands = wrap.execute(f"loadcmd {args[0]}") if len(args) > 0 else [config.LOADFILE, []]
    commands = _commands[1] if len(_commands) > 1 else []
    variables = {"PS1": ">>> ", "_": "DTC"} 
    in_command = len(commands) != 0
    i = 0
    while True:
        PS1, CONST_LANG = _default_vars(variables)
        variables["CONST_LANG"] = CONST_LANG
        if not in_command:
            try:
                command = input(PS1)
            except:
                print()
                command = "exit"
        else:
            command = commands[i]
        args = wrap.execute(command, vars=variables)
        syscode = args if type(args) == int else args[0]
        other = []
        if type(args) != int and len(args) > 1:
            other = args[1:]
        if syscode == config.SYSEXIT and not in_command:
            break
        elif syscode == config.SYSEXIT and in_command:
            commands = []
            i = 0
            in_command = not in_command
            continue
        elif syscode == config.GLOBEXIT: # it terminate work anywhere :)
            break
        elif syscode == config.EXPORTVAR:
            if len(other) == 2:
                if other[0] != None:
                    if other[1] != None:
                        variables[other[0]] = other[1]
                    else:
                        variables[other[0]] = " "
                else:
                    functions.info(f"{locale.get_by_token(tokens.EXPORT_VAR_IS_NULL)}", level='e')
            else:
                functions.info(f"{locale.get_by_token(tokens.NO_EXPORT_INFO)}", level='e')
            # try:
            #     variables[other[0]] = other[1]
            # except Exception as e:
            #     functions.info(f"{locale.get_by_token(tokens.VAR_EXPORT_ERROR)} {e}", level='e')
        elif syscode == config.NOCOMMAND:
            functions.info(f"{locale.get_by_token(tokens.NO_SUCH_COMMAND)} {command.split()[0]}")
        elif syscode == config.CONTINUE:
            pass
        elif syscode == config.LOADFILE:
            commands = other[0]
            in_command = len(commands) != 0
            i = 0
            continue    
        else:
            functions.info(f"{locale.get_by_token(tokens.ERRROR_SYSCODE_UNREGISTERED)} {syscode}", level='w')
        
        if len(commands) - 1 != i:
            i += 1
        else:
            in_command = False
    functions.info(f"{locale.get_by_token(tokens.EXIT_EXPECTED)}", level="d")