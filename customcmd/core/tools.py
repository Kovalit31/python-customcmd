from string import punctuation
from . import config

def parse_vars(args: str, variables: dict):
    args_new = []
    have_symbols = False
    have_variable_name = False
    is_variable = False
    is_string = False
    _temp_str = ""
    _temp_var = ""
    new_punctuation = " "
    for x in range(len(punctuation)):
        if not punctuation[x] == config.VARIABLE_PREFIX and not punctuation[x] == config.STRING_1 and not punctuation[x] == config.STRING_2:
            new_punctuation += punctuation[x]
    new_punctuation = new_punctuation.strip()
    for x in range(len(args)):
        if args[x] in new_punctuation:
            if is_variable:
                is_variable = False
                have_symbols, _temp_str = __add_to_output(_temp_str, have_symbols, _temp_var, variables)
                have_symbols, _temp_str = __add_to_str_or_new(_temp_str, args[x], have_symbols)
                have_variable_name = False
            else:
                have_symbols, _temp_str = __add_to_str_or_new(_temp_str, args[x], have_symbols)
        elif args[x] == config.VARIABLE_PREFIX:
            if is_variable:
                have_symbols, _temp_str = __add_to_output(_temp_str, have_symbols, _temp_var, variables)
                have_variable_name = False
            else:
                is_variable = True
        elif args[x] == config.CMD_DELIMITER:
            if is_variable:
                is_variable = False
                have_symbols, _temp_str = __add_to_output(_temp_str, have_symbols, _temp_var, variables)
                have_variable_name = False
            if not is_string:
                have_symbols = False
                args_new.append(_temp_str)
            else:
                have_symbols, _temp_str = __add_to_str_or_new(_temp_str, " ", have_symbols)
        elif args[x] == config.STRING_1 or args[x] == config.STRING_2:
            if is_variable:
                is_variable = False
                have_symbols, _temp_str = __add_to_output(_temp_str, have_symbols, _temp_var, variables)
                have_symbols, _temp_str = __add_to_str_or_new(_temp_str, args[x], have_symbols)
                have_variable_name = False
            else:
                have_symbols, _temp_str = __add_to_str_or_new(_temp_str, args[x], have_symbols)
            is_string = True
        else:
            if is_variable:
                have_variable_name, _temp_var = __add_to_str_or_new(_temp_var, args[x], have_variable_name)
            else:
                have_symbols, _temp_str = __add_to_str_or_new(_temp_str, args[x], have_symbols)
    if have_symbols:
        args_new.append(_temp_str)
    if have_variable_name:
        value = __find_vars_value(_temp_var, variables)
        if value == None and not have_symbols:
            args_new.append(f"{config.VARIABLE_PREFIX}{_temp_var}")
        elif value == None and have_symbols:
            args_new[-1] += f"{config.VARIABLE_PREFIX}{_temp_var}"
        elif value != None and have_symbols:
            args_new[-1] += value
        else:
            args_new.append(value)
    return args_new

def __add_to_str_or_new(old: str, add: str, have: bool) -> tuple[bool, str]:
    _temp_str = str(add) if not len(str(old)) > 0 or not have else str(old) + str(add)
    if len(_temp_str) > 0:
        return True, _temp_str
    else:
        return False, _temp_str
    
def __find_vars_value(variable: str, variables: dict):
    variable_keys = []
    for x in variables.keys():
        variable_keys.append(x)
    if not variable in variable_keys:
        return
    return variables[variable]

def __add_to_output(orig_str: str, have: bool, var_name: str, variables: dict):
    value = __find_vars_value(var_name, variables)
    if value == None:
        have_symbols, newstr = __add_to_str_or_new(orig_str, f"{config.VARIABLE_PREFIX}{var_name}", have)
    else:
        have_symbols, newstr = __add_to_str_or_new(orig_str, value, have)
    return have_symbols, newstr
