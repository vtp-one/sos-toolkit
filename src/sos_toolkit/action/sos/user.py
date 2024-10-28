from typing import Optional, Annotated
from pydantic import Field
import rich

from os import environ
from pathlib import Path

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo
from sos_toolkit.meta import _global

@sos_action
def user(
    file: Annotated[Optional[str], Field(description="The file to set for sos-user.yaml")] = None,
):

    """NOT IMPLEMENTED - Set the location for an sos-user.yaml file"""
    rich.print({"SOS_USER":
            {
            "file":file
            }
        })

    raise NotImplementedError()
    #
    # TODO
    # - need a way to persist this file
    # - could write it into root but that is messy for development
    # - could include it in sos-local but that requires a sos-system
    # - could use XDG directory
    # - want to write to env variable but that requires cli command
    # - no easy way?
    #

    if file.lower() == "none":
        environ.pop(_global.ENV_SYSTEM_FILE, None)

    else:
        file = Path(file).absolute()

        # test file is valid
        __CTX__ = SOSContext.generate(
            system_file=False,
            local_file=False,
            user_file=file,
            root_file=False)

        # THIS DOES NOT PERSIST OUTSIDE OF THE CURRENT INTREPRETER RUN
        #environ[_global.ENV_SYSTEM_FILE] = file.as_posix()

    return ResultRepo(user_file=file)
