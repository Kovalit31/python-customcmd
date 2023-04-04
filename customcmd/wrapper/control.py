import types
from ..core import config
from . import wrap
from ..tools import functions
from ..locale import locale, tokens
from ..tools import pathutil

def find_index(arr: list, what) -> int:
    for x in range(len(arr)):
        if arr[x] == what:
            return x
    return None

def read_cmds(path: str) -> list:
    _path = pathutil.is_file_throw(path)
    if path == None:
        return []
    commands = []
    try:
        file = open(_path, "r", "utf-8")
        commands = file.readlines()
        file.close()
    except Exception as e:
        return []
    return commands

class Wrap():
    
    modules = []
    call_names = []
    end = []
    unpackable = []
    returns_code = []
    command = " "
    # variables = []
    # values = []
    variables = dict()
    
    def __init__(self) -> None:
        self.variables["PS1"] = ">>> "
    
    def load_module(self, module: types.FunctionType, callname: str, after=config.CONTINUE, unpack_output=False, returns_code=False):
        if not type(module) == types.FunctionType:
            return
        self.modules.append(module)
        self.call_names.append(str(callname))
        self.end.append(after)
        self.unpackable.append(unpack_output)
        self.returns_code.append(returns_code)
    
    def exec(self):
        if self.command.strip() == "":
            return
        _cmd = self.command.strip().split(" ")
        _self_cmd = _cmd[0].lower()
        _cmd_args = []
        index = find_index(self.call_names, _self_cmd)
        if index == None:
            return config.NOCOMMAND
        _vars_keys = []
        for x in self.variables.keys():
            _vars_keys.append(x)
        if len(_cmd) > 1:
            _temp = _cmd[1:]
            for x in range(len(_temp)):
                if _temp[x].startswith("$"):
                    if _temp[x].lstrip("$") in _vars_keys:
                        _cmd_args.append(self.variables[_temp[x].lstrip("$")])
                    else:
                        _cmd_args.append(" ")
                else:
                    _cmd_args.append(_temp[x])
        return wrap.exec(self.modules[index], self.end[index], fnreturns_code=self.returns_code[index], _cmd_args=_cmd_args, fnunpack=self.unpackable[index])
        
    
    def run(self, args: list):
        commands = read_cmds(args[0]) if len(args) > 0 else []
        in_command = len(commands) > 0
        iterator = 0
        while True:
            try:
                self.command = input(self.variables["PS1"]) if not in_command else commands[iterator]
            except KeyboardInterrupt or EOFError:
                break
            _ret = self.exec()
            code = _ret[0] if not type(_ret) == int else _ret
            other = _ret[1:] if type(_ret) != int and len(_ret) > 1 else []
            if code == config.SYSEXIT and not in_command:
                break
            elif code == config.SYSEXIT and in_command:
                commands = []
                i = 0
                in_command = not in_command
                continue
            elif code == config.GLOBEXIT: # it terminate work anywhere :)
                break
            elif code == config.EXPORTVAR:
                if len(other) == 2:
                    if other[0] != None:
                        if other[1] != None:
                            self.variables[other[0]] = other[1]
                        else:
                            self.variables[other[0]] = " "
                    else:
                        functions.info(f"{locale.get_by_token(tokens.EXPORT_VAR_IS_NULL)}", level='e')
                else:
                    functions.info(f"{locale.get_by_token(tokens.NO_EXPORT_INFO)}", level='e')
            elif code == config.NOCOMMAND:
                functions.info(f"{locale.get_by_token(tokens.NO_SUCH_COMMAND)} {self.command.split()[0]}")
            elif code == config.CONTINUE:
                pass
            elif code == config.LOADFILE:
                commands = other[0]
                in_command = len(commands) != 0
                i = 0
                continue    
            else:
                functions.info(f"{locale.get_by_token(tokens.ERRROR_SYSCODE_UNREGISTERED)} {code}", level='w')
                
            if in_command:
                iterator += 1
                if len(commands) == iterator:
                    in_commands = not in_commands