import types
from ..core import config

def exec(function: types.FunctionType, return_code: int, fnreturns_code=False, _cmd_args=[], fnunpack = False):
    try:
        ret = function(_cmd_args)
        _return = ret if type(ret) != int or ret != None else [ret]
        _final = tuple()
        code = return_code if not fnreturns_code else _return[0] if len(_return) > 0 else config.CONTINUE
        _final += tuple([code])
        if fnunpack:
            for x in range(len(_return[1:]) + 1 if len(_return) > 1 else 0):
                _final += tuple([_return[x]])
        return _final
    except KeyboardInterrupt or EOFError:
        return config.SYSEXIT
    except Exception as e:
        return config.CONTINUE, e
