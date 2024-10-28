from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def load():

    """NOT IMPLEMENTED - Load a System"""
    rich.print({"SOS_LOAD":True})

    raise NotImplementedError()
