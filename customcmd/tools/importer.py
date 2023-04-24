import importlib.util
import sys
import types

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
