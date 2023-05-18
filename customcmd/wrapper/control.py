import copy
import os
import types
from . import wrap
from ..core import config
from ..tools import functions, importer, global_functions
from ..locale import locale

class Wrap():
    modules = dict()
    commands = dict()
    sh_variables = dict()
    functions = []
    callnames = []
    endcode = []
    unpack = []
    retcode = []
    get = []
    _command = " "

    
    def __init__(self) -> None:
        self.tokenizer = importer.import_module(config.DEFAULT_TOKENIZER, os.path.join(os.path.dirname(__file__), "tokenizers", config.DEFAULT_TOKENIZER)+".py")
        self.sh_variables["PS1"] = "%u@%h:%d\$"
        self.sh_variables["LANG"] = config.DEFAULT_LANG
    
    def load_module(self, module: types.ModuleType, modulename: str): #, after=config.CONTINUE, unpack_output=False, returns_code=False, get_self=False
        if not type(module) == types.ModuleType:
            return
        if modulename in global_functions.get_dict_keys(self.modules):
            return
        self.modules[modulename] = []
        for x in dir(module):
            if not x.startswith("_") and type(getattr(module, x)) == types.FunctionType:
                if x in self.functions:
                    if not functions.interactive("Oops: There was an dublicate of function!", "Do you want to continue? [y]es/[n]o"):
                        return
                    else:
                        self.unload_function(x)
                self.load_function(getattr(module, x), x)
                self.modules[modulename].append(len(self.functions) - 1)
    
    def unload_module(self, module_name: str) -> None:
        try:
            a = copy.deepcopy(self.modules[module_name])
        except:
            return
        b = copy.deepcopy(self.callnames)
        for x in range(len(a)):
            self.unload_function(b[a[x]])
        self.modules.pop(module_name, None)
    
    def load_function(self, function: types.FunctionType, callname: str, endcode=config.SYS_EXEC_CONTINUE, unpack=False, retcode=False, get=False) -> None:
        if type(function) != types.FunctionType:
            return
        if callname in self.callnames:
            return
        if function in self.functions:
            return
        self.functions.append(function)
        self.callnames.append(callname)
        self.endcode.append(endcode)
        self.unpack.append(unpack)
        self.retcode.append(retcode)
        self.get.append(get)
        
    def edit_function(self, callname: str, callname_new = None, after=None, unpack=None, retcode=None, get=None) -> None:
        try:
            i = self.callnames.index(callname)
        except ValueError:
            return
        _func = self.functions[i]
        _callname = callname_new if callname_new != None else self.callnames[i]
        _after = after if after != None else self.endcode[i]
        _unpack = unpack if unpack != None else self.unpack[i]
        _retcode = retcode if retcode != None else self.retcode[i]
        _get = get if get != None else self.get[i]
        self.unload_function(callname)
        self.load_function(_func, _callname, endcode=_after, unpack=_unpack, retcode=_retcode, get=_get)
    
    def unload_function(self, callname: str) -> None:
        try:
            i = self.callnames.index(callname)
        except ValueError:
            return
        self.functions.pop(i)
        self.callnames.pop(i)
        self.endcode.pop(i)
        self.unpack.pop(i)
        self.retcode.pop(i)
        self.get.pop(i)
        _exit = False
        for y in self.modules.keys():
            for z in range(len(self.modules[y])):
                if self.modules[y][z] == i:
                    self.modules[y].pop(z)
                    _exit = True
                    break
            if _exit:
                break
    
    def exec(self):
        if self._command.strip() == "":
            return config.CONTINUE
        _cmd_data = self.tokenizer.cmd_parse(self._command, self.sh_variables)
        try:
            index = self.callnames.index(_cmd_data[0])
        except:
            index = None
        if index == None:
            return config.SYS_EXEC_CMD_NFOUND
        return wrap.exec(self.functions[index], self.endcode[index], fnreturns_code=self.retcode[index], _cmd_args=_cmd_data, fnunpack=self.unpack[index])
        
    def run(self, args: list):
        commands = functions.read_from_file(args[0]) if len(args) > 0 else []
        in_command = len(commands) > 0
        iterator = 0
        while True:
            try:
                curlang = self.sh_variables["LANG"].lower()[0:2]
                _fileslang = locale.get_current()
                fileslang = _fileslang if _fileslang == None else _fileslang.strip() 
                if not curlang == fileslang:
                    if locale.set_lang(curlang):
                      global_functions.info(f"{locale.get_by_token('locale.reload.trigger')}") 
                else:
                    pass
            except:
                pass
            try:
                self._command = input(self.tokenizer.ps1_parse(self.sh_variables["PS1"], tuple([self.callnames, self.functions]), variables = self.sh_variables)) if not in_command else commands[iterator]
            except KeyboardInterrupt or EOFError:
                print() # The fix :)
                break
            _ret = self.exec()
            code = _ret[0] if not type(_ret) == int else _ret
            other = _ret[1:] if type(_ret) != int and len(_ret) > 1 else []
            if code == config.SYS_EXEC_STOP and not in_command:
                break
            elif code == config.SYS_EXEC_STOP and in_command:
                commands = []
                # i = 0
                in_command = not in_command
                continue
            elif code == config.SYS_EXEC_FORCESTOP: # it terminate work everywhere :)
                break
            elif code == config.SHELL_VARS_EXPORT:
                if len(other) == 2:
                    if other[0] != None:
                        if other[1] != None:
                            self.sh_variables[other[0]] = other[1]
                        else:
                            self.sh_variables[other[0]] = " "
                    else:
                        global_functions.info(f"{locale.get_by_token('error.export.variable.isnull')}", level='e')
                else:
                    global_functions.info(f"{locale.get_by_token('error.export.variable.littleinfo')}", level='e')
            elif code == config.SYS_EXEC_CMD_NFOUND:
                global_functions.info(f"{locale.get_by_token('error.command.unexpected')} {self._command.split()[0]}")
            elif code == config.SYS_EXEC_CONTINUE:
                pass
            elif code == config.SYS_EXEC_EXECFILE:
                commands = other[0]
                in_command = len(commands) != 0
                i = 0
                continue
            elif code == config.SYS_MODULE_LOAD:
                _path = other[0]
                _name = "_".join(os.path.basename(_path).split(".")[:-1].split(" "))
                _tmp_module = importer.import_module(_name, _path)
                self.load_module(_tmp_module, _name)
                importer.unimport_module(_tmp_module, _name)
            elif code == config.SYS_MODULE_UNLOAD:
                _modname = other[0]
                self.unload_module(_modname)
            elif code == config.SYS_FUNCTION_LOAD:
                pass
            elif code == config.SYS_FUNCTION_UNLOAD:   # TODO: Create function loading and unloading
                pass
            elif code == config.SYS_FUNCTION_SETUP:
                pass
            else:
                global_functions.info(f"{locale.get_by_token('error.syscode.unregistered')} {code}", level='w')
                
            if in_command:
                iterator += 1
                if len(commands) == iterator:
                    in_commands = not in_commands
