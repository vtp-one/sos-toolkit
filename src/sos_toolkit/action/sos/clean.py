from typing import Optional, Annotated
from pydantic import Field
import rich

from os import remove as os_remove
from os.path import exists as path_exists

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo, _global

@sos_action
def clean(
    target: Annotated[Optional[str], Field(description="The context object to target")] = "",
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
):

    """Clean up a System"""
    rich.print({"SOS_CLEAN":
            {
            "target":target,
            "context_file":context_file
            }
        })

    __CTX__ = SOSContext.file_load(context_file=context_file)

    _target = "action.sos_clean"
    if target != "":
        _target = ".".join([_target, target])

    result = __CTX__.run(_target)

    file = __CTX__.get("meta.context_file")

    if path_exists(file):
        if _global.ALLOW_DELETE:
            rich.print(f"DELETING CONTEXT FILE: {file}")
            os_remove(file)

        else:
            rich.print(f"TEST DELETE CONTEXT FILE: {file}")

    return result
