from typing import Optional, Annotated, Callable
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def commit(
    target: Annotated[Optional[str], Field(description="The commit object to target")] = "default",
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
):

    """Commit System objects"""
    rich.print({"SOS_COMMIT":
            {
            "target":target,
            "context_file":context_file,
            }
        })

    __CTX__ = SOSContext.file_load(context_file=context_file)

    result = __CTX__.run(f"action.sos_commit.{target}")

    __CTX__.file_save()
    return result
