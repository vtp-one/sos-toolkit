from typing import Optional, Annotated, Literal, Dict
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, sos_tool
import rich

from ._client import get_client

# TODO
# - unpack run_kwargs for annotation
@sos_tool
def network_create(
    name: Annotated[str, Field(description="Name for Network")],
    kwargs: Annotated[dict, Field(description="Additional Kwargs for Create")] = {},
    exists_error: Annotated[bool, Field(description="If Network Exists Error")] = False
):
    """Create a Docker Network"""
    rich.print({"docker.network_create":
            {
            "name":name,
            "kwargs":kwargs,
            "exists_error":exists_error
            }
        })

    client = get_client()

    _name = name in [z.name for z in client.network.list()]

    if exists_error is True and _name:
        e = f"NETWORK EXISTS ERROR: {name}"
        raise RuntimeError(e)

    elif _name:
        result = client.network.inspect(name)

    else:
        kwargs.pop("name", None)
        result = get_client().network.create(name=name, **kwargs)

    return {"result":result}

@sos_tool
def network_remove(
    name: Annotated[str, Field(description="Name for Network")],
    kwargs: Annotated[dict, Field(description="Additional Kwargs")] = {},
    not_exists_error: Annotated[bool, Field(description="If Network Does not Exist Error")] = False
):
    """Remove a Docker Network"""
    rich.print({"docker.network_create":
            {
            "name":name,
            "kwargs":kwargs,
            "not_exists_error":not_exists_error
            }
        })

    client = get_client()

    _name = name in [z.name for z in client.network.list()]
    if not_exists_error is True and not _name:
        e = f"NETWORK DOES NOT EXIST: {name}"

    elif not _name:
        result = None

    else:
        #kwargs.pop("name", None)
        #n = client.network.inspect(name, **kwargs)
        n = client.network.inspect(name)
        result = client.network.remove(n)

    return {"result":result}

@sos_tool
def network_exists(
    name: Annotated[str, Field(description="Name of Network")],
    kwargs: Annotated[dict, Field(description="Additional Kwargs")] = {},
    not_exists_error: Annotated[bool, Field(description="If network does not exist error")] = False,

):
    """Check if a docker network exists"""
    rich.print({"docker.network_exists":
            {
            "name":name,
            "kwargs":kwargs,
            "not_exists_error":not_exists_error
            }
        })

    client = get_client()

    _exists = name in [z.name for z in client.network.list()]

    if not _exists and not_exists_error:
        e = f"DOCKER NETWORK DOES NOT EXIST: {name}"
        raise RuntimeError(e)

    return {"result":_exists}
