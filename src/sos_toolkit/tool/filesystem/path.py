from typing import Optional, Annotated, List, Union
from pydantic import Field
from collections.abc import MutableMapping
from sos_toolkit.meta import SOSContext, SOS_TOOL, sos_tool
import rich

from os import makedirs, listdir
from os.path import join as _path_join
from os.path import exists as _path_exists
from os.path import isdir as path_isdir
from pathlib import Path
from shutil import rmtree

@sos_tool
def path_join(
    __CTX__: Annotated[Optional[SOSContext], Field(description="SOSContext Object")],
    target: Annotated[List[str], Field(description="List of path segments for join")]
):

    """Join Path Segments"""
    rich.print({"filesystem.path_join":
            {"target":target
            }
        })

    for (n, obj) in enumerate(target):
        if isinstance(obj, str):
            if obj.startswith("__CTX__"):
                obj = __CTX__.get(obj.lstrip("__CTX__."))

        else:
            obj = __CTX__.get(obj)

        target[n] = obj

    return {"output":_path_join(*target)}

@sos_tool
def path_exists(
    target: Annotated[Union[str, List[str]], Field(description="Target Path")],
    raise_exc: Annotated[Optional[bool], Field(description="If Raise Exception")] = False
):
    """Test if Target Path Exists"""

    rich.print({"filesystem.path_exists":
        {
        "target":target,
        "raise_exc":raise_exc
        }
        })

    if not isinstance(target, list):
        target = [target]

    exists = [_path_exists(t) for t in target]
    _exists = all(exists)

    if not _exists and raise_exc:
        _target = []
        for (n, v) in enumerate(exists):
            if v is False:
                _target.append(target[n])

        e = f"PATH DOES NOT EXIST: {_target}"
        raise RuntimeError(e)

    return {"result":_exists}
