import os

from ..tools import global_functions, pathutil

PATH = os.path.join(os.path.dirname(__file__), "lang")

def get_by_token(token: str, lang=None) -> str:
    '''
    Gets language value with token
    '''
    path = os.path.join(PATH, "c.po") if lang == None else os.path.join(PATH, f"{lang}.po")
    if not os.path.exists(path):
        global_functions.info(f"Developer! No such locale: {'default' if lang == None else lang}!", level="e")
        return f"{{{token}}}"
    try:
        file = open(path, "r", encoding="utf-8")
        data = file.readlines()
        file.close()
    except Exception as e:
        global_functions.info(f"Can't get locale! {e}", level='e')
        return f"{{{token}}}"
    lang = data[0].strip().lower() if lang == None else lang
    __parse_po(data[1:])
    for x in range(len(data)):
        if data[x].strip() == token.lower().strip():
            try:
                return data[x+1].strip()
            except Exception as e:
                global_functions.info(f"Developer! File {f'{lang}.po'} not fully edited!", level="d")
                return f"{{{token}}}"
    else:
        global_functions.info(f"Developer! File {f'{lang}.po'} doesn't content {token}!", level='d')
        return f"{{{token}}}"

def set_lang(lang: str) -> bool:
    '''
    Set @param lang as default language
    '''
    data = []
    if pathutil.is_file_throw(os.path.join(PATH, f"{lang}.po")) != None:
        try:
            file = open(pathutil.get_full_path(os.path.join(PATH, f"{lang}.po")), "r", encoding="utf-8")
            data = file.readlines()
            file.close()
        except Exception as e:
            global_functions.info(f"Developer! Can't open file with lang {lang}, because this error occurs: {e}", level="d")
            return False
        try:
            file = open(os.path.join(PATH, "c.po"), "w", encoding="utf-8") 
            file.write(f"{lang}\n" + "".join(data))
            file.close()
        except Exception as e:
            global_functions.info(f"Developer! Can't create default locale file, because this error occurs: {e}", level="d")
            return False
    else:
        global_functions.info(f"{get_by_token('tokens.NO_SUCH_LOCALE')} {lang}", level="e")
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
            global_functions.info(f"Developer! Can\'t get current locale: {e}", level='d')
            return None
        return curlang
    else:
        global_functions.info("Developer! c.po is not file or doesn't exists!", level='d')
        return None

def __parse_po(data: list[str]) -> tuple[list[dict], list[str], dict]:
    _data: list[dict] = []
    for x in range(len(data)):
        if data[x].strip().startswith('~'):
            _temp = data[x].strip()[1:].split(".")
            for y in range(len(_temp)):
                if len(_data) == y:
                    _data.append(dict())
                if not ".".join(_temp[:y]+[_temp[y]]) in global_functions.get_dict_keys(_data[y]):
                    if y == 0:
                        _data[y][_temp[y]] = []
                        continue
                    _data[y-1][".".join(_temp[:y-1]+[_temp[y-1]])].append(".".join(_temp[:y]+[_temp[y]]))
                    _data[y][".".join(_temp[:y]+[_temp[y]])] = []
                    if y == len(_temp) - 1:
                        _data[y][".".join(_temp[:y]+[_temp[y]])].append(data[x+1]) if len(data) > x else _data[y][".".join(_temp[:y]+[_temp[y]])].append("")
                    continue
                # if not _temp[y] in _saved_keys:
                #     _saved_keys.append(_temp[y])
                #     _aliases[_temp[y]] = _saved_keys.index(_temp[y])
                # if not y == 0:
                #     _data[y-1][_aliases[_temp[y-1]]].append(_aliases[_temp[y]])
                # _data[y][_aliases[_temp[y]]] = [] if not _aliases[_temp[y]] in global_functions.get_dict_keys(_data[y]) else global_functions.do_nothing()
    print(_data)
                