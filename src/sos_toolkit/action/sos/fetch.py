from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def fetch(
    target: Annotated[Optional[str], Field(description="The context object to target")] = "",
):

    """NOT IMPLEMENTED - Fetch the remote objects for a System"""
    rich.print({"SOS_FETCH":
            {
            "target":target,
            }
        })

    __CTX__ = SOSContext.file_load(context_file=context_file)

    _target = "action.sos_fetch"
    if target != "":
        _target = ".".join([_target, target])

    result = __CTX__.run(_target)

    __CTX__.file_save()
    return result
