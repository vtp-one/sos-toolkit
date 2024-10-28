from typing import Optional, Annotated
from pydantic import Field
import rich

from os import getcwd
from os.path import join as path_join
from urllib.parse import urlparse

from sos_toolkit.meta import SOS_TOOL, sos_action, ResultRepo

@sos_action
def pull(
    remote_target: Annotated[Optional[str], Field(description="Remote Git Repo to Pull")] = None,
    local_target: Annotated[Optional[str], Field(description="Local Folder to use or create")] = "",
    remote_branch: Annotated[Optional[str], Field(description="Remote Branch to Pull")] = "main",
    force: Annotated[bool, Field(default=False, description="If folder exists DELETE it before pull")] = False
):

    """Pull a System from a Git Target"""
    rich.print({"SOS_PULL":
            {"remote_target":remote_target,
             "local_target":local_target,
             "remote_branch":remote_branch,
             "force":force
            }
        })

    target = urlparse(remote_target)

    if not target.path.endswith(".git"):
        e = f"TARGET NOT VALID GIT REPO: {target}"

    remote_target_name = target.path.split("/")[-1].removesuffix(".git")

    #
    # TODO
    # - try and keep local target from deleting everything
    # - local_target = "/"
    #
    if local_target == "":
        local_target = path_join(getcwd(), remote_target_name)

    else:
        local_target = path_join(getcwd(), local_target)

    result = ResultRepo()

    exists = SOS_TOOL.filesystem.directory_exists(local_target)["result"]

    if force and exists:
        SOS_TOOL.filesystem.directory_delete(local_target)

    elif exists:
        rich.print(f"TARGET DIRECTORY EXISTS: {local_target}")
        return

    SOS_TOOL.filesystem.directory_create(local_target)

    SOS_TOOL.git.repo_clone(
        remote_target=remote_target,
        local_target=local_target,
        remote_branch=remote_branch)

    return result
