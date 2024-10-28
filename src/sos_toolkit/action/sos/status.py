from typing import Optional, Annotated, Callable
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def status(
    target: Annotated[Optional[str], Field(description="The context object to target")] = "",
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
):

    """Get the Status of System Objects"""
    rich.print({"SOS_STATUS":
            {
            "target":target,
            "context_file":context_file
            }
        })

    __CTX__ = SOSContext.file_load(context_file=context_file)

    _target = "action.sos_status"
    if target != "":
        _target = ".".join([_target, target])

    result = __CTX__.run(_target)
    __CTX__.file_save()
    return result
