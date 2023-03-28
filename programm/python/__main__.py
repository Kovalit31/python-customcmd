import sys

def info(string: str, level="i", debug=True) -> None:
    '''
    Wraps output
    @param string (str): Output string
    @param level (str): Info level ([d]ebug|[i]nfo|[e]rror|[w]arning|[f]atal) (Default: i)
    '''
    _level = level.lower().strip()
    if _level == 'd' and not debug:
        return
    print(f"[{'*' if _level == 'i' else '!' if _level == 'w' else '@' if _level == 'e' else '~' if _level == 'd' else '&'}] {string}")
    if _level == 'f':
        raise Exception(string.capitalize())

def wrapper(command: str) -> int:
    if command == "exit" or command == "quit":
        return 0
    return 1

def main(args: list) -> None:
    commands = [] # Need to save file...
    _continue = True
    if len(args) > 0:
        info("Trying to process file")
        info(f"File: {args[0]}", level='d')
        try:
            file = open(args[0], "r")
            commands = file.readlines()
            file.close()
        except Exception as e:
            info(f"Can't process file: {e}", level='e')
        if len(commands) > 0:
            for x in commands:
                signal = wrapper(x)
                if signal == 0:
                    _continue = False
                if not _continue:
                    break
    while _continue:
        command = input()
        signal = wrapper(command)
        if signal == 0:
            break
    info("Exit expected!", level="d")

if __name__ == "__main__":
    main(sys.argv[1:])