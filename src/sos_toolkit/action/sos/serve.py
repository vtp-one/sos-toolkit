from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def serve():

    """NOT IMPLEMENTED - Start an API Server in an SOSContext"""
    rich.print({"SOS_SERVE":True})

    raise NotImplementedError()
