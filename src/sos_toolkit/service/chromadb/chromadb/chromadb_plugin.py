from typing import Optional, Annotated, Any, Union, List
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, ResultObject, sos_tool

import rich


@sos_tool
def debug(
):
    """Test Plugin for Service Installations"""

    rich.print({"chromadb.debug":True})

    return True
