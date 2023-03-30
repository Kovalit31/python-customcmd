import sys
from . import tools
from . import wrapper

info = tools.functions.info

def main(args: list) -> None:
    wrapper.control.command_processor(args)

if __name__ == "__main__":
    main(sys.argv[1:])