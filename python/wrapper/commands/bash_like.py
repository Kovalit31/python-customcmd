from ...tools import functions, pathutil
from ...locale import locale, tokens

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
    
def read(args: list) -> tuple[str, str]:
    '''
    Reads standart input to get value of variable
    '''
    if len(args) < 1:
        functions.info(f"{locale.get_by_token(tokens.FEW_ARGS_FOR_READ)}")
        return None, None
    inputted = input(args[1] if len(args) > 1 else "")
    return args[0], inputted

def exec(args: list) -> list:
    '''
    Gets command list from file
    '''
    if len(args) < 1:
        functions.info(f"{locale.get_by_token(tokens.FEW_ARGS_FOR_LOAD)}", level='e')
        return []
    path = pathutil.is_file_throw(args[0])
    if path == None:
        return []
    functions.info(f"{locale.get_by_token(tokens.FILE_OPEN_TRY)}")
    functions.info(f"{locale.get_by_token(tokens.FILE_NAME_DISPLAY)} {args[0]}", level='d')
    commands = []
    try:
        file = open(path, "r")
        commands = file.readlines()
        file.close()
    except Exception as e:
        functions.info(f"{locale.get_by_token(tokens.ERROR_FILE_READ)} {e}", level='e')
    return commands