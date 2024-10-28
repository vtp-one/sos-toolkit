from typing import Optional, Annotated, Literal, Dict
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, sos_tool
import rich

from ._client import get_client

# TODO
# - unpack run_kwargs for annotation
@sos_tool
def container_run(
    image: Annotated[str, Field(description="Image for Container")],
    run_kwargs: Annotated[dict, Field(description="Additional Kwargs for Run")] = {}
):
    """Run a Container"""
    rich.print({"docker.container_run":
            {
            "image":image,
            "run_kwargs":run_kwargs
            }
        })

    container = get_client().run(image=image, **run_kwargs)

    return {"container":container}

@sos_tool
def container_stop(
    name: Annotated[str, Field(description="Container Name to Stop")],
    stop_kwargs: Annotated[dict, Field(description="Additional Kwargs for Stop")] = {}
):
    """Stop a Container"""
    rich.print({"docker.container_stop":
            {
            "name":name,
            "stop_kwargs":stop_kwargs
            }
        })

    get_client().container.stop(name, **stop_kwargs)

    return True

@sos_tool
def container_running(
    name: Annotated[str, Field(description="Container Name to Check")]
):
    """Check if a container with the name is running"""

    raise NotImplementedError()
