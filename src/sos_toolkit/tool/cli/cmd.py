from typing import Optional, Annotated, Any, List, Dict
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, ResultObject, sos_tool

import rich

import plumbum

@sos_tool
def cmd_popen(
    cmd: Annotated[str, Field(description="The Target CLI Command")],
    args: Annotated[Optional[List[str]], Field(description="List of args for the command")] = [],
    kwargs: Annotated[Optional[Dict[str,str]], Field(description="Dict of kwargs for the Popen Constructor")] = {}
):
    """Run the target CMD with the provided args"""
    rich.print({"cli.cmd_popen":
            {"cmd":cmd,
             "args":args,
             "kwargs":kwargs
             }
        })

    _cmd = getattr(plumbum.cmd, cmd)

    accumulator = []
    for line in _cmd.popen(args=tuple(args), **kwargs):
        accumulator.append(line)
        rich.print(line)

    return {"output":accumulator}
