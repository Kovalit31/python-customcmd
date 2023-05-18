from customcmd.tools import global_functions
import os
import string 

VARIABLE_PREFIX = "$"
CMD_DELIMITER = " "
STRING_1 = "\""
STRING_2 = "'"

def ps1_parse(ps1: str, functions: tuple[list, list], variables: dict = dict()) -> str:
    return ps1 if not 'pwd' in functions[0] else functions[1][functions[0].index("pwd")]([], _return_path = True) + "$"

def cmd_parse(args: str, variables: dict):
    mapped = []
    in_var = False
    in_str_double = False
    in_str_once = False
    _tstro = ""
    _tstrd = ""
    _tvar = ""
    _available_vars = global_functions.get_dict_keys(variables)
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
                if not in_str_double and len(_tstrd) > 0:
                    mapped[-1] = global_functions.clever_add_str(mapped[-1], _tstrd)
                    _tstrd = ""
                    continue
        elif args[x] == STRING_2:
            if not in_str_double:
                in_str_once = not in_str_once
                if not in_str_once and len(_tstro) > 0:
                    mapped[-1] = global_functions.clever_add_str(mapped[-1], _tstro)
                    _tstro = ""
                    continue
        elif args[x] == CMD_DELIMITER:
            if not (in_str_double or in_str_once):
                mapped.append("")
                continue        
        if in_str_double:
            _tstrd = global_functions.clever_add_str(_tstrd, args[x])
        elif in_str_once:
            _tstro = global_functions.clever_add_str(_tstrd, args[x])
        else:
            mapped[-1] = global_functions.clever_add_str(mapped[-1], args[x])
            
    return mapped
    # STEP 2: PARSE VARS
    for x in range(len(mapped)):
        for y in range(len(mapped[x])):
            pass