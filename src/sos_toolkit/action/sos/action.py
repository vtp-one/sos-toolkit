from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def action(
    target: Annotated[Optional[str], Field(description="The action object to target")] = "",
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
):

    """Run the Target Object from an SOSContext"""
    rich.print({"SOS_ACTION":
            {
            "action":action
            }
        })

    __CTX__ = SOSContext.file_load(context_file=context_file)

    result = __CTX__.run(target)

    __CTX__.file_save()
    return result
