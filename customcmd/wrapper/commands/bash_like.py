from customcmd.core import config
from customcmd.tools import global_functions, pathutil
from customcmd.locale import locale

def export(args: list) -> tuple[str, str]:
    '''
    Exports variable
    @return variable - Variable
    @return value - Value of
    Works as bash's export
    '''
    _var = None
    _val = None
    _parsed = " ".join(args[1:])
    start, end = global_functions.char_count(_parsed, "=")
    if end - start > 0:
        return None, None
    _var, _val = _parsed.split("=", maxsplit=1)
    return _var.strip(), _val.strip()
    
def read(args: list) -> tuple[str, str]:
    '''
    Reads standart input to get value of variable
    '''
    args = args[1:]
    if len(args) < 1:
        global_functions.out(f"{locale.get_by_token('exec.cmd.read.error.fewargs')}")
        return None, None
    inputted = input(args[1] if len(args) > 1 else "")
    return args[0], inputted

def exec(args: list) -> list:
    '''
    Gets command list from file
    '''
    args = args[1:]
    if len(args) < 1:
        global_functions.out(f"{locale.get_by_token('exec.cmd.load.error.fewargs')}", level='e')
        return []
    path = pathutil.is_file_throw(args[0])
    if path == None:
        return []
    global_functions.out(f"{locale.get_by_token('tokens.FILE_OPEN_TRY')}")
    global_functions.out(f"{locale.get_by_token('tokens.FILE_NAME_DISPLAY')} {args[0]}", level='d')
    commands = []
    try:
        file = open(path, "r")
        commands = file.readlines()
        file.close()
    except Exception as e:
        if config.EXTRA_DEBUG:
            raise e
        global_functions.out(f"{locale.get_by_token('tokens.ERROR_FILE_READ')} {e}", level='e') # TODO Replace all tokens.
    return commands
