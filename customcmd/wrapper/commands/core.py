def null(_: list):
    '''
    Nullable function. Does nothing.
    '''
    pass

def returning(args: list) -> list:
    '''
    Returns back all args
    '''
    return args[1:]

# Note: returning function need to be unloaded and it need to be added with other callname!
