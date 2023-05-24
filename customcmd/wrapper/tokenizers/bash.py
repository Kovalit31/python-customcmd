from customcmd.tools import global_functions
import string 
import copy

VARIABLE_PREFIX = "$"
CMD_DELIMITER = " "
STRING_1 = "\""
STRING_2 = "'"

def ps1_parse(ps1: str, functions: dict, variables: dict = dict()) -> str:
    return ps1 if not 'pwd' in global_functions.get_dict_keys(functions) else functions['pwd'][0]([], _return_path = True) + "$"

def cmd_parse(args: str, variables: dict):
    mapped = []
    in_str_double = False
    in_str_once = False
    _tstro = ""
    _tstrd = ""
    latest = -1
    punctuation = []
    for x in range(len(string.punctuation)):
        if not string.punctuation[x] in [VARIABLE_PREFIX, CMD_DELIMITER, STRING_1, STRING_2]:
            punctuation.append(string.punctuation[x])
    # STEP 1: PARSE STRINGS
    for x in range(len(args)):
        if len(mapped) == 0:
            mapped.append("")
        if args[x] == STRING_1:
            if not in_str_once:
                in_str_double = not in_str_double
                if in_str_double:
                    latest = x
                if not in_str_double and len(_tstrd) > 0:
                    mapped[-1] = global_functions.clever_add_str(mapped[-1], _tstrd)
                    _tstrd = ""
            else:
                _tstro = global_functions.clever_add_str(_tstro, args[x])
        elif args[x] == STRING_2:
            if not in_str_double:
                in_str_once = not in_str_once
                if in_str_once:
                    latest = x
                if not in_str_once and len(_tstro) > 0:
                    mapped[-1] = global_functions.clever_add_str(mapped[-1], _tstro)
                    _tstro = ""
            else:
                _tstrd = global_functions.clever_add_str(_tstrd, args[x])
        elif args[x] == CMD_DELIMITER:
            if not (in_str_double or in_str_once):
                mapped.append("")
        else:
            if in_str_double:
                _tstrd = global_functions.clever_add_str(_tstrd, args[x])
            elif in_str_once:
                _tstro = global_functions.clever_add_str(_tstro, args[x])
            else:
                mapped[-1] = global_functions.clever_add_str(mapped[-1], args[x])
    if in_str_once ^ in_str_double:
        mapped[-1] = global_functions.clever_add_str(mapped[-1], args[latest])
    elif in_str_once or in_str_double:
        global_functions.out("It's confusing! Double and once quote strings are in use! Are you freak?", level='f')
    # STEP 2: PARSE VARS
    _tvar = ""
    _other = ""
    invar = False
    _available_vars = global_functions.get_dict_keys(variables)
    # return mapped
    for x in range(len(mapped)):
        _temp = copy.copy(mapped[x])
        for y in range(len(_temp)):
            if _temp[y] == VARIABLE_PREFIX:
                if len(_tvar) > 0 and _tvar in _available_vars:
                    _other = global_functions.clever_add_str(_other, variables[_tvar])
                invar = True
                _tvar = ""
            elif _temp[y] in punctuation:
                if invar:
                    invar = False
                    if _tvar in _available_vars:
                        _other = global_functions.clever_add_str(_other, variables[_tvar])
                _other = global_functions.clever_add_str(_other, _temp[y])
            else:
                if invar:
                    _tvar = global_functions.clever_add_str(_tvar, _temp[y])
                else:
                    _other = global_functions.clever_add_str(_other, _temp[y])
        mapped[x] = _other
        _other = ""

    return mapped
