from ...tools import functions, pathutil
from ...locale import locale, tokens
from ...core import config

import os

def create_db(args: list):
    '''
    Create DB partitioning 
    @param args[0] - File
    @param args[1] - DB id
    @param args[2] - (optional) DB sign
    '''
    if functions.return_if_few(args, 1, msg=tokens.FEW_ARGS_FOR_CREATEDB):
        return
    path = pathutil.get_full_path(args[0], return_else=True)
    if os.path.exists(path):
        if not functions.interactive(locale.get_by_token(tokens.NEED_REPLACE_FILE), locale.get_by_token(tokens.CONTINUE_QUESTION), _additional=args[0]):
            return
    db_id = args[1] if len(args) > 1 else input(f"{locale.get_by_token(tokens.NEED_FOR_DB_ID)} ")
    db_sign_persist = False
    db_sign_text = ""
    db_sign_line_count = 0
    if len(args) > 2:
        db_sign_text = " ".join(args[2:]).replace("\\", "\n")
        db_sign_line_count = len(db_sign_text.split("\n"))
        db_sign_persist = not db_sign_persist
    else:
        if functions.interactive(locale.get_by_token(tokens.CAN_SIGN_DB), locale.get_by_token(tokens.IF_SIGN_DB)):
            db_sign_persist = not db_sign_persist
            functions.info(f"{locale.get_by_token(tokens.PLEASE_SET_SIGN_DATA)}")
            while True:
                db_sign_line_count += 1
                db_sign_text = functions.add_or_set_str(db_sign_text, input().strip().replace("\\", "\n"))
                if not db_sign_text.endswith("\n"):
                    break
    db_data = functions.add_to_string_with_nl(str(config.VERSION), config.DEFAULT_LANG)
    db_data = functions.add_to_string_with_nl(db_data, db_id)
    if db_sign_persist:
        db_data = functions.add_to_string_with_nl(db_data, "s")
        db_data = functions.add_to_string_with_nl(db_data, str(db_sign_line_count))
        db_data = functions.add_to_string_with_nl(db_data, db_sign_text)
    db_data = functions.add_to_string_with_nl(db_data, str(0))
    db_data = functions.add_to_string_with_nl(db_data, ".")
    db_data = functions.add_to_string_with_nl(db_data, str(0))
    functions.write_to_file(path, db_data)

def create_vdb():
    pass

def load_db():
    pass

def load_vdb():
    pass

def unload_db():
    pass

def unload_vdb():
    pass

def print_db():
    pass

def print_vdb():
    pass

def remove_vdb():
    pass

def remove_db():
    pass

# keys 

# def add_key():
#     pass

# def remove_key():
#     pass

# def edit_key():
#     pass

# def print_key():
#     pass

def ls():
    pass

def rmkey():
    pass

def rmdir():
    pass

def cd():
    pass

def mkdir():
    pass

def addkey():
    pass


'''
The comments

version
s/u - signed/unsigned
if s, Sign len
if s, sign
db name
vdb count
<db structure without vdb>
.
num of files/dirs
d/f (dir/file)
__init__.py -|
num of keys -| file
d/f (dir/file)
__pycache__       -| 
num of files/dirs -| dirs
dbend
'''