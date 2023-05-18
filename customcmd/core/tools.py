# from . import config

# def __add_to_str_or_new(old: str, add: str, have: bool) -> tuple[bool, str]:
#     _temp_str = str(add) if not len(str(old)) > 0 or not have else str(old) + str(add)
#     if len(_temp_str) > 0:
#         return True, _temp_str
#     else:
#         return False, _temp_str
    
# def __find_vars_value(variable: str, variables: dict):
#     variable_keys = []
#     for x in variables.keys():
#         variable_keys.append(x)
#     if not variable in variable_keys:
#         return
#     return variables[variable]
