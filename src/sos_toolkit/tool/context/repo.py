from typing import Optional, Annotated, Any, Dict, Literal, Callable
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, ResultObject, sos_tool, ToolRepo, ToolObject

import rich

@sos_tool
def repo_remove(
    namespace: Annotated[str, Field(description="ToolRepo namespace for the tool")]
):
    """Remove a tool repo"""
    rich.print({"context.repo_remove":
            {
            "namespace":namespace,
            }
        })

    SOS_TOOL.remove(namespace)

    return True
