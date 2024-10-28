from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def config(
    target: Annotated[Optional[str], Field(description="The config object to target")] = "",
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
):

    """Configure the System SOSContext"""
    rich.print({"SOS_CONFIG":
            {
            "target":target,
            "context_file":context_file
            }
        })

    __CTX__ = SOSContext.file_load(context_file=context_file)

    if target == "":
        _target = "action.sos_config.default"

        if not __CTX__.has(_target):
            _target = "action.sos_config"

    elif target.startswith("service"):
        _target = target.split(".")
        _target = f"service.{_target[1]}.sos_config.{_target[2]}"

    else:
        _target = f"action.sos_config.{target}"

    result = __CTX__.run(_target)

    __CTX__.file_save()
    return result
