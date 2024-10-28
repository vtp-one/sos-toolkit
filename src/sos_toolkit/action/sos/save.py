from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def save():

    """NOT IMPLEMENTED - Save a System"""
    rich.print({"SOS_SAVE":True})

    raise NotImplementedError()
