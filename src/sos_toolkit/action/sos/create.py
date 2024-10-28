from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def create():

    """NOT IMPLEMENTED - Create a System"""
    rich.print({"SOS_CREATE":True})

    raise NotImplementedError()
