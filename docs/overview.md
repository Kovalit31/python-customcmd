# Overview

## System

wrapper.control.Wrap() - Main runners constructor

It's .run(args) method allows to start interactive console.

The wrapper.commands package contains modules (see [modules](modules.md)), what contains functions
This functions can be imported with .import_module()

## Error codes and print handling

### Error codes

- core.config.SYSEXIT: Exit from runner
- core.config.CONTINUE: Continue executing files
- core.config.NOCOMMAND: Prints message about not command found
- core.config.LOADFILE: Go ahead and import script to execute
- core.config.GLOBEXIT: Exit from runner, ignors top-levels
- core.config.EXPORTVAR: Export variable to shell

### Print handling

Print handles with tools.functions.info(), what have error levels:

- e: Error
- i: Info
- d: Debug
- f: Fatal, raises Exception with string as message
- v: Verbose
- w: Warning

Also it might to use full name of verbosity or register dance, roles won't be different.
