from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def web():

    """NOT IMPLEMENTED - Start a Web UI in an SOSContext"""
    rich.print({"SOS_WEB":True})

    raise NotImplementedError()
