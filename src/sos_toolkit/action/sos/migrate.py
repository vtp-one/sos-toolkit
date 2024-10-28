from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def migrate(
    version: Annotated[Optional[str], Field(description="The version to target")] = "",
):

    """NOT IMPLEMENTED - Migrate a System"""

    rich.print({"SOS_MIGRATE":
            {
            "target":target,
            }
        })

    raise NotImplementedError("SOS_MIGRATE")
