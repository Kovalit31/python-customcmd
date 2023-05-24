import os
import sys
from ..core import config

# =====================
#  Internal algorithms
# =====================


# def binary_search(where: list, what) -> tuple[int, int]:
#     where.sort()
#     _arr = copy.deepcopy(where)
#     while True:
#         if len(_arr) == 0:
#             return -1, -1
#         if _arr[math.floor(len(_arr)/2)-1] < what:
#             _arr = _arr[math.floor(len(_arr)/2)-1:]
#         elif _arr[math.floor(len(_arr)/2)-1] > what:
#             _arr = _arr[:math.floor(len(_arr)/2)-1]
#         else:
#             return math.floor(len(_arr)/2)-1, math.floor(len(_arr)/2)-1

# =====================
#         UE
# =====================

def out(string: str, level="i") -> None:
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

def get_resolution() -> tuple[int, int]:
    return os.get_terminal_size().columns(), os.get_terminal_size().lines()

# ==================
#  String functions
# ==================

def clever_add_str_nl(_first: str, _second: str) -> str:
    return _first + "\n" + _second

def clever_add_str(_str: str, _add: str) -> str:
    if _str == None or _str == "":
        return _add
    else:
        return _str + _add

def str_to_list(string: str) -> list:
    return [string[x] for x in range(len(string))]

def char_count(string: str, char: str) -> int:
    list_of = str_to_list(string)
    list_of.sort()
    try:
        start = list_of.index(char)
        end = list_of[::-1].index(char)
        return start, len(list_of)-1-end
    except Exception as e:
        return -1, -1

# ==================
#       Other
# ==================

def do_nothing() -> None:
    pass

def get_dict_keys(dictionary: dict) -> list:
    if not type(dictionary) == dict:
        return []
    output = []
    for x in dictionary.keys():
        output.append(x)
    return output

def get_list_from_to_including(arr: list, end: int, start: int = 0) -> list:
    return arr[start:end]+[arr[end]]