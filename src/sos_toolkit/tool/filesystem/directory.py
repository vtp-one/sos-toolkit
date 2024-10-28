from typing import Optional, Annotated
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, sos_tool, _global
import rich

from os import makedirs, listdir
from os.path import exists as path_exists
from os.path import isdir as path_isdir
from pathlib import Path
from shutil import rmtree

@sos_tool
def directory_exists(target: Annotated[str, Field(description="Target Directory to Check")]):
    """Check if a Directory Exists"""
    rich.print({"filesystem.directory_exists":
            {"target":target
            }
        })
    return {"result":path_exists(target) and path_isdir(target)}

@sos_tool
def directory_delete(
    target: Annotated[str, Field(description="Target Directory to Delete")],
    ignore_errors: Annotated[bool, Field(description="If ignore errors on delete")] = False,
):
    """Delete a Target Directory"""
    rich.print({"filesystem.directory_delete":
            {"target":target,
             "ignore_errors":ignore_errors,
            }
        })

    if path_exists(target) and path_isdir(target):
        if _global.ALLOW_DELETE:
            rich.print(f"DELETE DIRECTORY: {target}")
            rmtree(target, ignore_errors)

        else:
            rich.print(f"TEST DELETE DIRECTORY: {target}")

    else:
        if ignore_errors:
            pass

        else:
            e = f"INVALID PATH - target: {target}"
            raise RuntimeError(e)

    return {"result":True}

@sos_tool
def directory_create(
    target: Annotated[str, Field(description="Target Directory to Create")],
    mode: Annotated[int, Field(description="The Unix Permission Mode")] = 0o777,
    exist_ok: Annotated[bool, Field(description="If already exists error")] = False
):
    """Create a Target Directory"""
    rich.print({"filesystem.directory_create":
            {"target":target,
             "mode":mode,
             "exist_ok":exist_ok
            }
        })

    makedirs(target, mode, exist_ok)

    #
    # TODO
    # - get this correct
    #
    return {"path":str(Path(target).absolute())}

@sos_tool
def directory_list(
    target: Annotated[str, Field(description="Target Directory to List")] = None
):
    """Return a list of a directory contents"""
    rich.print({"filesystem.directory_list":
            {"target":target
            }
        })

    return {"list":listdir(target)}
