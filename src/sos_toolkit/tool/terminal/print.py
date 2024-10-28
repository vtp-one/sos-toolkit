from typing import Optional, Annotated, Any
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, ResultObject, sos_tool

import rich
import rich.rule

@sos_tool
def print_result(
    __RESULT__: Annotated[ResultObject, Field(description="ResultObject")],
    horizontal_rule: Annotated[bool, Field(description="If wrap the output in horizontal rules")] = False
):
    """Print a ResultObject to the terminal"""
    rich.print({"terminal.print_result":True})

    if horizontal_rule:
        rich.print(rich.rule.Rule())

    __RESULT__.print()

    if horizontal_rule:
        rich.print(rich.rule.Rule())

    return True

@sos_tool
def print_object(
    obj: Annotated[Any, Field(description="Object to Print")],
    horizontal_rule: Annotated[bool, Field(description="If wrap the output in horizontal rules")] = False
):
    """Print any object to the terminal"""
    if horizontal_rule:
        rich.print(rich.rule.Rule())

    rich.print({"terminal.print_object":obj})

    if horizontal_rule:
        rich.print(rich.rule.Rule())

    return True

@sos_tool
def print_context(
    __CTX__: Annotated[Optional[SOSContext], Field(description="SOSContext Object")],
    ctx_target: Annotated[Optional[str], Field(description="Target Object to Print")] = None,
    horizontal_rule: Annotated[bool, Field(description="If wrap the output in horizontal rules")] = False
):
    """Print the current context to the terminal"""
    rich.print({"terminal.print_context":
            {
            "ctx_target":ctx_target
            }
        })

    if horizontal_rule:
        rich.print(rich.rule.Rule())

    if ctx_target is not None:
        rich.print(__CTX__.get(ctx_target, None))

    else:
        __CTX__.print()

    if horizontal_rule:
        rich.print(rich.rule.Rule())

    return True

@sos_tool
def print_callback(
    horizontal_rule: Annotated[bool, Field(description="If wrap the output in horizontal rules")] = False
):
    """Create a Callback to Print the SOSContext"""
    rich.print({"terminal.print_callback":True})
    return ResultObject(callbacks=[{"tool":"terminal.print_context", "params":{"horizontal_rule":horizontal_rule}}])
