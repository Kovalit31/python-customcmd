# Overview

## System

wrapper.control.Wrap() - Main runners constructor

It's .run(args) method allows to start interactive console.

The wrapper.commands package contains modules (see [modules](modules.md)), what contains functions
The modules with this functions can be imported with .import_module()

## Error codes and print handling

### Error codes

- core.config.SYS_EXEC_STOP: Exit from runner
- core.config.SYS_EXEC_CONTINUE: Continue executing files
- core.config.SYS_EXEC_CMD_NFOUND: Prints message about not command found
- core.config.SYS_EXEC_EXECFILE: Go ahead and import script to execute
- core.config.SYS_EXEC_FORCESTOP: Exit from runner, ignors top-levels
- core.config.SYS_VARS_EXPORT: Export variable to shell
- core.config.SYS_MODULE_LOAD: Loads a module            |
- core.config.SYS_MODULE_UNLOAD: Unloads module          |
- core.config.SYS_FUNCTION_LOAD: Loads function          | - Many ways used by another built-in functions, but without these codes
- core.config.SYS_FUNCTION_UNLOAD: Unloads function      |
- core.config.SYS_FUNCTION_EDIT: Setups to edit function |

### Print handling

Print handles with tools.functions.info(), what have error levels:

- e: Error
- i: Info
- d: Debug
- f: Fatal, raises Exception with string as message
- v: Verbose
- w: Warning

Also it might to use full name of verbosity or register dance, roles won't be different.
