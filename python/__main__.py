import sys
from . import tools
from . import wrapper
from . import core

info = tools.functions.info

def main(args: list) -> None:
    loader = wrapper.control.Wrap()
    loader.load_module(wrapper.commands.unix_like.ls, 'ls')
    loader.load_module(wrapper.commands.unix_like.echo, 'echo')
    loader.load_module(wrapper.commands.unix_like.cd, 'cd')
    loader.load_module(wrapper.commands.unix_like.exit, 'exit', after=core.config.SYSEXIT)
    loader.load_module(wrapper.commands.bash_like.exec, 'exec', after=core.config.LOADFILE, unpack_output=True)
    loader.load_module(wrapper.commands.bash_like.read, 'read', after=core.config.EXPORTVAR, unpack_output=True)
    loader.load_module(wrapper.commands.bash_like.export, 'export', after=core.config.EXPORTVAR, unpack_output=True)
    loader.run(args)

if __name__ == "__main__":
    main(sys.argv[1:])