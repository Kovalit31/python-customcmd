from ..core import config
from ..locale import locale
from . import pathutil, global_functions

# ===================
#   User experience
# ===================

def interactive(action: str, question: str, yes_locall=locale.get_by_token("user.ue.action.answer.yes"), no_locall=locale.get_by_token("user.ue.action.answer.no"), yes_eng = locale.get_by_token("user.ue.action.answer.yes", lang="en"), no_eng = locale.get_by_token("user.ue.action.answer.no", lang="en"), _additional=None) -> bool:
    answer = input(f"{action}{' ' +_additional if not _additional == None else ''}. {question} ").lower()
    yes_l = yes_locall.lower()
    yes_d = yes_eng.lower()
    no_l = no_locall.lower()
    no_d = no_eng.lower()
    first_nl = no_l[0] if len(no_l) > 0 else ""
    first_nd = no_d[0] if len(no_d) > 0 else ""
    first_yl = yes_l[0] if len(yes_l) > 0 else ""
    first_yd = yes_d[0] if len(yes_d) > 0 else ""
    first_la = answer[0] if len(answer) > 0 else first_yd
    if not (first_la == first_nl or first_la == first_nd) and (first_la == first_yl or first_la == first_yd):
        return True
    else:
        return False

# =================
#   File handling
# =================

def write_to_file(path: str, text: str) -> None:
    try:
        file = open(path, "w", encoding='utf-8')
        file.write(text)
        file.close()
    except Exception as e:
        if config.EXTRA_DEBUG:
            raise e
        global_functions.out(f"{locale.get_by_token('io.path.file.action.write.error').format(file=path, error=e)}", level='e')

def read_from_file(path: str) -> None:
    realpath = pathutil.is_file_throw(path)
    if realpath == None:
        return []
    try:
        file = open(realpath, 'r',  encoding='utf-8')
        ret = file.readlines()
        file.close()
        return ret
    except Exception as e:
        if config.EXTRA_DEBUG:
            raise e
        return [] # TODO: Read error

# ==================
#       Other
# ==================

def return_if_few(args: list, minlen: int, msg: str = "") -> bool:
    if len(args) < minlen:
        global_functions.out(f"{locale.get_by_token(msg)}", level="e") if len(msg) > 0 else global_functions.do_nothing()
        return True
    return False
