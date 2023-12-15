import argparse
from typing import Optional
import pwndbg.lib
import pwndbg.commands
import pwndbg.gdblib.proc
import pwndbg.gdblib.config
from pwndbg.color import message
from pwndbg.commands import CommandCategory
from pwndbg.commands.attachp import attachp

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawTextHelpFormatter,
    description="""attachp wrapper""",
)
parser.add_argument("target", nargs="?", type=str, help="pid, process name or device file to attach to", default=None)

_prev_attached = None
@pwndbg.commands.ArgparsedCommand(parser, category=CommandCategory.START)
def at(target: Optional[str]) -> None:
    global _prev_attached
    if pwndbg.gdblib.proc.alive:
        print(message.warn("already attached"))
        return
    if target is None:
        target = _prev_attached
    if target is None:
        print(message.error("No target specified"))
        return
    attachp(False, target)
    if pwndbg.gdblib.proc.alive:
        _prev_attached = target
