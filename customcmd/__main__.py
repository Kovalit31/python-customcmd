import sys
from . import tools
from . import wrapper
from . import core

info = tools.functions.info

def main(args: list) -> None:
    loader = wrapper.control.Wrap()
    loader.load_module(wrapper.commands.unix_like, "unix_like")
    loader.load_module(wrapper.commands.bash_like, "bash_like")
    loader.load_function(wrapper.commands.core.null, "exit", endcode=core.config.SYS_EXEC_STOP)
    loader.edit_function("exec", after=core.config.SYS_EXEC_EXECFILE, unpack=True)
    loader.edit_function("read", after=core.config.SHELL_VARS_EXPORT, unpack=True)
    loader.edit_function("export", after=core.config.SHELL_VARS_EXPORT, unpack=True)
    loader.run(args)

if __name__ == "__main__":
    main(sys.argv[1:])
