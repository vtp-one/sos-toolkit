from typing import Union, Optional, Annotated, Literal, List
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, sos_tool, _global
import rich

from ._client import get_client
import python_on_whales as POW

@sos_tool
def volume_exists(
    target: Annotated[str, Field(description="Name of the Volume")],
    client_config: Annotated[dict, Field(description="The Docker Client Config dict")] = {}
):
    """Check if a volume exists"""
    rich.print({"docker.volume_exists":
            {
            "target":target,
            "client_config":client_config,
            }
        })

    return {"result":get_client(**client_config).volume.exists(target)}

@sos_tool
def volume_create(
    target: Annotated[str, Field(description="Name of the Volume")],
    volume_kwargs: Annotated[dict, Field(description="Volume Configuration")] = {},
    ignore_exists: Annotated[bool, Field(description="If ignore volume already exists")] = True,
    client_config: Annotated[dict, Field(description="The Docker Client Config dict")] = {},
):
    """Create a volume"""
    rich.print({"docker.volume_create":
            {
            "target":target,
            "client_config":client_config,
            }
        })

    c = get_client(**client_config)

    if not c.volume.exists(target):
        volume_kwargs["volume_name"] = target
        c.volume.create(**volume_kwargs)

    elif ignore_exists:
        pass

    else:
        e = f"VOLUME ALREADY EXISTS: {target}"
        raise RuntimeError(e)

    return True

@sos_tool
def volume_delete(
    target: Annotated[str, Field(description="Name of the Volume")],
    ignore_missing: Annotated[bool, Field(description="If ignore image does not exist")] = True,
    client_config: Annotated[dict, Field(description="The Docker Client Config dict")] = {}
):
    """Delete a Colume"""
    rich.print({"docker.volume_delete":
            {
            "target":target,
            "ignore_missing":ignore_missing,
            "client_config":client_config,
            }
        })

    c = get_client(**client_config)

    if _global.ALLOW_DELETE:
        rich.print(f"DELETE VOLUME: {target}")

        if c.volume.exists(target):
            c.volume.remove(target)

        elif ignore_missing:
            pass

        else:
            e = f"VOLUME DOES NOT EXIST: {target}"
            raise RuntimeError(e)

    else:
        rich.print(f"TEST VOLUME DELETE: {target}")


    return {"result":True}
