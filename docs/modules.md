# Modules

## Usage

Modules is developed to:

- Help users and developers write additional code for this commandline interpreter
- Simple usage (deleted one module, inserted another one...)

This modules CAN NOT be used in:

- Telemetry
- User scaming

...and so one

## Development of modules

Modules is developed from functions.

Function need to be with following signature:

```python3
def name(args: list):
    pass # Some code
```

args is post-processed arguments for command.

## Installing

First, need to add module in __init__.py (it may forbidden, if you won't do it)
Then need to add this to main file:

```python3
loader.load_module(module, "modulename")
```

or (if you have custom main):

```python3
import sys
import customcmd.wrapper.control
loader = control.Wrap()
# Code above
loader.run(sys.argv)
```

If you wish to edit function parametrs or it's callname, you need for this:

```python3
loader.edit_function("callname") # And parametrs
```

If you want import only function, do it same as it was in v1.0.0

```python3
loader.load_function(function, "cmdname") # And parametrs
```

Default callname for function is it's own name.

Also you can add after parameter, to add code after execution (see [overview](overview.md)'s Error codes),  
return unpacking (unusable) or returns_code, if your function returns code from Error codes.
