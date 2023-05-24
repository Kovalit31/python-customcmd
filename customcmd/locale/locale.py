import os
import shutil

from ..tools import global_functions, pathutil
from ..core import config

PATH = os.path.join(os.path.dirname(__file__), "lang")

def get_by_token(token: str, lang=None) -> str:
    '''
    Gets language value with token
    '''
    path = os.path.join(PATH, "c.po") if lang == None else os.path.join(PATH, f"{lang}.po")
    if not os.path.exists(os.path.join(PATH, "c.po")) or not os.path.isfile(os.path.join(PATH, "c.po")):
        set_lang(config.DEFAULT_LANG)
    try:
        file = open(path, "r", encoding="utf-8")
        data = file.readlines()
        file.close()
    except Exception as e:
        global_functions.out(f"Can't get locale! {e}", level='e')
        return f"{{{token}}}"
    lang = data[0].strip().lower() if lang == None else lang
    ret = __get_candidate(__parse_po(data[1:]), token)
    if ret == None:
        return f"{{{token}}}"
    candidate, auto = ret
    if auto != None:
        candidate = candidate.replace("{!auto}", auto)
    return candidate

def set_lang(lang: str) -> bool:
    '''
    Set @param lang as default language
    '''
    data = []
    if os.path.exists(os.path.join(PATH, "c.po")) and not os.path.isfile(os.path.join(PATH, "c.po")):
        shutil.rmtree(os.path.join(PATH, "c.po"))
    if os.path.exists(os.path.join(PATH, f"{lang}.po")):
        try:
            file = open(pathutil.get_full_path(os.path.join(PATH, f"{lang}.po")), "r", encoding="utf-8")
            data = file.readlines()
            file.close()
        except Exception as e:
            global_functions.out(f"Developer! Can't open file with lang {lang}, because this error occurs: {e}", level="d")
            return False
        try:
            file = open(os.path.join(PATH, "c.po"), "w", encoding="utf-8") 
            file.write(f"{lang}\n" + "".join(data))
            file.close()
        except Exception as e:
            global_functions.out(f"Developer! Can't create default locale file, because this error occurs: {e}", level="d")
            return False
    else:
        content = os.listdir(PATH)
        if not config.DEFAULT_LANG+".po" in content:
            global_functions.out(f"NO LANGS FOUND!", level='f')
        global_functions.out(f"{get_by_token('data.locale.error.po.nolang').format(lang=lang)}", level="e")
        return False
    return True

def get_current() -> str:
    if pathutil.is_file_throw(os.path.join(PATH, 'c.po')) != None:
        curlang = ''
        try:
            file = open(pathutil.get_full_path(os.path.join(PATH, 'c.po')), "r", encoding="utf-8")
            curlang = file.readlines()[0]
            file.close()
        except Exception as e:
            global_functions.out(f"Developer! Can\'t get current locale: {e}", level='d')
            return None
        return curlang
    else:
        global_functions.out("Developer! c.po is not file or doesn't exists!", level='d')
        return None

def __parse_po(data: list[str]) -> list[dict]:
    _data: list[dict] = []
    for x in range(len(data)):
        if data[x].strip().startswith('~'):
            _temp = data[x].strip()[1:].split(".")
            for y in range(len(_temp)):
                if len(_data) == y:
                    _data.append(dict())
                if not ".".join(global_functions.get_list_from_to_including(_temp, y)) in global_functions.get_dict_keys(_data[y]):
                    if y != 0:
                        _data[y-1][".".join(global_functions.get_list_from_to_including(_temp, y-1))].append(".".join(global_functions.get_list_from_to_including(_temp, y)))
                    _data[y][".".join(global_functions.get_list_from_to_including(_temp, y))] = [None]
                    if y == len(_temp) - 1:
                        _data[y][".".join(global_functions.get_list_from_to_including(_temp, y))][0] = data[x+1] if len(data) > x else ""
                else:
                    if len(_temp)-1 == y:
                        _data[y][".".join(global_functions.get_list_from_to_including(_temp, y))][0] = data[x+1] if len(data) > x else ""
    return _data

def __get_candidate(data: list[dict], token: str) -> str:
    _temp = token.strip().split(".")
    _next_token = str()
    auto = None
    for x in range(len(_temp)):
        if len(data) == x:
            return
        if not ".".join(global_functions.get_list_from_to_including(_temp, x)) in global_functions.get_dict_keys(data[x]):
            if x == 0:
                return
            if not ".".join(global_functions.get_list_from_to_including(_temp, x-1)+["*"]) in global_functions.get_dict_keys(data[x]):
                return
            else:
                auto = _temp[x]
                _temp[x] = "*"
        _next_token = ".".join(global_functions.get_list_from_to_including(_temp, x))
    else:
        if data[x][_next_token][0] == None:
            return
        return data[x][_next_token][0].strip("\n"), auto