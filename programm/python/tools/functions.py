from ..core import config

def info(string: str, level="i", debug=config.DEBUG) -> None:
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
        raise Exception(string.capitalize())

def char_count(string: str, char: str) -> int:
    count = 0
    for x in range(len(string)):
        if string[x] == char:
            count += 1
    return count