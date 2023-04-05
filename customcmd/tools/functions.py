from ..core import config
from ..locale import locale, tokens

def info(string: str, level="i") -> None:
    '''
    Wraps output
    @param string (str): Output string
    @param level (str): Info level ([d]ebug|[v]erbose|[i]nfo|[e]rror|[w]arning|[f]atal) (Default: i)
    '''
    _level = level[0].lower().strip()
    if _level == 'd' and not config.DEBUG:
        return
    if _level == 'v' and not config.VERBOSE:
        return
    print(f"[{'*' if _level == 'i' else '!' if _level == 'w' else '@' if _level == 'e' else '~' if _level == 'd' else '.' if _level == 'v' else '&'}] {string}")
    if _level == 'f':
        raise Exception(string)

def char_count(string: str, char: str) -> int:
    count = 0
    for x in range(len(string)):
        if string[x] == char:
            count += 1
    return count

def interactive(action: str, question: str, yes_locall=locale.get_by_token(tokens.ANSWER_YES), no_locall=locale.get_by_token(tokens.ANSWER_NO), yes_eng = locale.get_by_token(tokens.ANSWER_YES, lang="en"), no_eng = locale.get_by_token(tokens.ANSWER_NO, lang="en"), _additional=None) -> bool:
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
    # info(f"{first_la}: {first_nl}, {first_nd} ? {first_yl}, {first_yd}", level='d')
    if not (first_la == first_nl or first_la == first_nd) and (first_la == first_yl or first_la == first_yd):
        return True
    else:
        return False
    
def add_to_string_with_nl(_first: str, _second: str) -> str:
    return _first + "\n" + _second

def add_or_set_str(_str: str, _add: str) -> str:
    if _str == None or _str == "":
        return _add
    else:
        return _str + _add
    
def return_if_few(args: list, minlen: int, msg: str = tokens.FEW_ARGS_ALL) -> bool:
    if len(args) < minlen:
        info(f"{locale.get_by_token(msg)}", level="e")
        return True
    return False

def write_to_file(path: str, text: str) -> None:
    try:
        file = open(path, "w", encoding='utf-8')
        file.write(text)
        file.close()
    except Exception as e:
        info(f"{locale.get_by_token(tokens.FILE_WRITE_ERROR)} {e}", level='e')