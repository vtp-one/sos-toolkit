from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def profile(
    profile: Annotated[Optional[str], Field(description="The profile to select")] = None,
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
):

    """Set the System Profile"""
    rich.print({"SOS_PROFILE":
            {
            "profile":profile,
            "context_file":context_file,
            }
        })

    __CTX__ = SOSContext.file_load(context_file=context_file)

    _target = "action.sos_profile"
    if profile != "":
        _target = ".".join([_target, profile])

    result = __CTX__.run(_target)

    __CTX__.meta.profile = profile
    __CTX__.file_save()
    return result
