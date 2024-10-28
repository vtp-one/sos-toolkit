from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def purge():

    """NOT IMPLEMENTED - Purge a System"""
    rich.print({"SOS_PURGE":True})

    raise NotImplementedError()
