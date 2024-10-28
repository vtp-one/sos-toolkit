from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def tool():

    """NOT IMPLEMENTED - Run an SOS-Toolkit Tool"""
    rich.print({"SOS_TOOL":True})

    raise NotImplementedError()
