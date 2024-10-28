from typing import Optional, Annotated, Callable
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

from os import getcwd

@sos_action
def help(
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
):

    """System Help Function"""
    rich.print({"SOS_HELP":
            {
            "context_file":context_file
            }
        })

    __CTX__ = None

    try:
        __CTX__ = SOSContext.file_load(context_file=context_file)

    except FileNotFoundError:
        e = f"CONTEXT FILE NOT FOUND - context_file: {context_file} - CHECKING FOR SYSTEM FILE"
        rich.print(e)

    if __CTX__ is None:
        try:
            __CTX__ = SOSContext.generate()

        except RuntimeError:
            e = f"SYSTEM FILE NOT FOUND IN CURRENT DIRECTORY - {getcwd()} - CHECKING FOR ROOT CONTEXT"
            rich.print(e)

    if __CTX__ is None:
        __CTX__ = SOSContext.generate(system_file=False)

    __CTX__.meta.print()

    supported_actions = [z for z in __CTX__.action.keys() if z.startswith("sos")]

    rich.print({"supported actions":supported_actions if len(supported_actions) else None})

    result = __CTX__.run("action.sos_help")

    return result
