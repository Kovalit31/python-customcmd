from . import unix_like
from . import bash_like

try:
    from .base import *
    BASE_IMPORTED = True
except:
    BASE_IMPORTED = False