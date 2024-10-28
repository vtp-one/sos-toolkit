from typing import Union, Optional, Annotated, Literal, List
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, sos_tool, _global
import rich

from ._client import get_client
import python_on_whales as POW

@sos_tool
def image_load(
    target: Annotated[Union[str, List[str]], Field(description="The target to load from")],
    tags: Annotated[Union[str, List[str]], Field(description="Tags to add to the image")] = [],
    source: Annotated[Literal["file", "url", "registry"], Field(description="The source type to load from")] = "file",
    client_config: Annotated[dict, Field(description="The Docker Client Config dict")] = {}
):
    """Load a Docker Image from a Target"""

    rich.print({"docker.image_load":
            {
            "source":source,
            "target":target,
            "client_config":client_config
            }
        })

    docker = get_client(**client_config)

    _target = target if isinstance(target, list) else [target]
    _tags = tags if isinstance(tags, list) else [tags]

    if len(_tags) and len(_tags) != len(_target):
        e = f"INVALID NUMBER OF TAGS: MUST PROVIDE A TAG OR NONE WHEN APPLYING TAGS"
        raise RuntimeError(e)

    match source:
        case "file":
            for n,t in enumerate(_target):
                z = docker.image.load(_target)

                if len(_tags):
                    docker.image.tag(z[0], _tags[n])

        case "url":
            raise NotImplementedError()
            #
            # request.get(url) => tempfile
            # dockerimage.load(tempfile)

        case "registry":
            docker.image.pull(_target)

            if len(_tags):
                for n,t in enumerate(_tags):
                    docker.image.tag(_tags[n], t)

        case _:
            e = f"INVALID IMAGE SOURCE: {source}"
            raise RuntimeError(e)

    return {
            "source":source,
            "target":target,
            "client_config":client_config
            }

@sos_tool
def image_exists(
    target: Annotated[str, Field(description="Tag for the Target Image")],
    client_config: Annotated[dict, Field(description="The Docker Client Config dict")] = {}
):
    """Check if an image exists"""
    rich.print({"docker.image_exists":
            {
            "target":target,
            "client_config":client_config,
            }
        })

    return {"result":get_client(**client_config).image.exists(target)}

@sos_tool
def image_delete(
    target: Annotated[str, Field(description="Tag for the Target Image")],
    force: Annotated[bool, Field(description="If force remove image")] = False,
    prune: Annotated[bool, Field(description="If prune untagged parent images")] = False,
    ignore_missing: Annotated[bool, Field(description="If ignore image does not exist")] = True,
    client_config: Annotated[dict, Field(description="The Docker Client Config dict")] = {}
):
    """Remove an Image"""
    rich.print({"docker.image_delete":
            {
            "target":target,
            "force":force,
            "prune":prune,
            "ignore_missing":ignore_missing,
            "client_config":client_config,
            }
        })

    try:
        if _global.ALLOW_DELETE:
            rich.print(f"DELETE IMAGE: {target}")
            get_client(**client_config).image.remove(target, force=force, prune=prune)

        else:
            rich.print(f"TEST IMAGE DELETE: {target}")

    except POW.exceptions.NoSuchImage:
        if ignore_missing:
            pass

        else:
            raise


    return {"result":True}
