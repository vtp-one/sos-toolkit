from typing import Optional, Annotated, Callable
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def context(
    target: Annotated[Optional[str], Field(description="The context object to target")] = "",
    context_file: Annotated[Optional[str], Field(description="The target context file")] = "",
    value: Annotated[Optional[str], Field(description="The value to set")] = "",
):

    """Query the System SOSContext"""
    rich.print({"SOS_CONTEXT":
            {
            "context_file":context_file,
            "target":target,
            "value":value,
            }
        })

    __CTX__ = SOSContext.file_load(context_file=context_file)

    result = __CTX__.run("action.sos_context")

    if target !=  "":
        if value != "":
            __CTX__.set(target, value, True)
            __CTX__.file_save()

        else:
            rich.print(f"TARGET: {target}")
            obj = __CTX__.get(target)
            try:
                obj.print()

            except:
                rich.print(obj)

    else:
        __CTX__.print()

    result.set("__CTX__", __CTX__)

    return result
