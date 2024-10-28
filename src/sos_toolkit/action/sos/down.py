from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def down(
    target: Annotated[Optional[str], Field(description="The context object to target")] = "",
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
):

    """Stop a System"""
    rich.print({"SOS_DOWN":
            {
            "target":target,
            "context_file":context_file
            }
        })

    __CTX__ = SOSContext.file_load(context_file=context_file, install_state=True)

    _target = "action.sos_down"
    if target != "":
        _target = ".".join([_target, target])

    result = __CTX__.run(_target)

    __CTX__.file_save()
    return result
