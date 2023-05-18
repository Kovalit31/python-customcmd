import sys
import types
import random
import importlib.util
from string import ascii_letters, punctuation
from . import pathutil

# ===================
#      Modules
# ===================

def import_module(name: str, path: str) -> types.ModuleType:
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

def unimport_module(module: types.ModuleType, name: str) -> None:
    sys.modules.pop(name)
    del(module)

# ===================
#      Functions
# ===================

def import_function(function_name: str, path_to_module: str) -> types.FunctionType:
    realpath = pathutil.is_file_throw(path_to_module)
    name = "".join([random.choice(ascii_letters+punctuation) for _ in range(15)])
    _temp = import_module(name, realpath)
    data = dir(_temp)
    _temp_fn = None
    if function_name in data and type(getattr(_temp, function_name)) == types.FunctionType:
        _temp_fn = getattr(_temp, function_name)
    unimport_module(_temp, name)
    return _temp_fn