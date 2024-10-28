from typing import Optional, Annotated, Callable
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo
from sos_toolkit.meta import SOSContext, ResultRepo

from sos_toolkit.root import TOOLKIT_PATH

import git

@sos_action
def version(
    target: Annotated[Optional[str], Field(description="The target SOS-Toolkit version")],
):

    """Change SOS-Toolkit Version"""
    rich.print({"SOS_VERSION":
        {
        "target":target
        }
    })

    # get system dir
    # should error if not a repo
    repo = git.repo.Repo(TOOLKIT_PATH)

    # update the repo
    # TODO:
    # - this should not crash when network is unavailable
    # - need to handle that somehow
    # - check network first?
    repo.git.pull()

    # change branch
    repo.git.checkout(target)

    return True
