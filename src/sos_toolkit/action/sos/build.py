from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def build(
    target: Annotated[Optional[str], Field(description="The build object to target")] = "",
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
):

    """Build System Objects"""
    rich.print({"SOS_BUILD":
            {
            "target":target,
            "context_file":context_file
            }
        })

    __CTX__ = SOSContext.file_load(context_file=context_file)

    _target = "action.sos_build"
    if target != "":
        _target = ".".join([_target, target])

    result = __CTX__.run(_target)

    __CTX__.meta.is_installed = True
    __CTX__.file_save()
    return result
