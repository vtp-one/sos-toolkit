from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def restart(
    target: Annotated[Optional[str], Field(description="The context object to target")] = "",
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
):

    """Restart a System"""
    rich.print({"SOS_RESTART":
            {
            "context_file":context_file
            }
        })

    __CTX__ = SOSContext.file_load(context_file=context_file, install_state=True)

    if target == "":
        result = ResultRepo()
        result.set("down", __CTX__.run("action.sos_down"))
        result.set("restart", __CTX__.run("action.sos_restart.default"))
        result.set("up", __CTX__.run("action.sos_up"))

    else:
        _target = f"action.sos_restart.{target}"
        result = __CTX__.run(_target)

    __CTX__.file_save()
    return result
