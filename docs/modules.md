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
Then need to add this:

```python3
loader.load_module(function, "cmdname")
```

to __main__.py

Also you can add after parameter, to add code after execution (see [overview](overview.md)'s Error codes),  
return unpacking (unusable) or returns_code, if your function returns code from Error codes.
