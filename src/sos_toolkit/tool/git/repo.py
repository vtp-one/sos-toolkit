from typing import Optional, Annotated
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, sos_tool
import rich
import rich.rule

import git

@sos_tool
def repo_clone(
    remote_target: Annotated[str, Field(description="The remote git repo")],
    local_target: Annotated[str, Field(description="The local folder to clone into")],
    remote_branch: Annotated[Optional[str], Field(description="The branch to checkout after clone")] = None
):
    """Clone a Remote Git Repo to a Local Folder"""
    rich.print({"git.repo_clone":
            {"remote_target":remote_target,
             "local_target":local_target,
             "remote_branch":remote_branch
             }
        })

    try:
        repo = git.Repo(local_target)

        if repo.is_dirty():
            rich.print(f"[bold red]REPO DIRTY - NOT OVERWRITING:[/bold red] - {remote_target} - {local_target}")
            return {
                    "remote_target":remote_target,
                    "local_target":local_target,
                    "remote_branch":remote_branch,
                    "working_dir":repo.working_dir
                    }

    except git.NoSuchPathError:
        SOS_TOOL.get("filesystem.directory_create")(target=local_target)
        repo = git.Repo.clone_from(remote_target, local_target)

    except git.InvalidGitRepositoryError:
        repo = git.Repo.clone_from(remote_target, local_target)

    #repo.git.pull()
    repo.git.fetch()

    if remote_branch:
        repo.git.checkout(remote_branch)

    return {
            "remote_target":remote_target,
            "local_target":local_target,
            "remote_branch":remote_branch,
            "working_dir":repo.working_dir
            }

@sos_tool
def repo_status(
    working_dir: Annotated[str, Field(description="The working directory for the Repo")]
):
    """Get the Status of a Git Repo"""
    rich.print({"git.repo_status":
            {"working_dir":working_dir
             }
        })

    repo = git.Repo(working_dir)
    is_dirty = repo.is_dirty()

    cur_hash = repo.head.object.hexsha
    origin = repo.remotes.origin
    origin.fetch()

    try:
        new_hash = origin.refs[repo.active_branch.name].object.hexsha
        is_behind = cur_hash != new_hash
        is_head = False

    except:
        # TODO
        # - this should only catch the detatched head error not all errors
        is_behind = False
        is_head = True

    state = ["REPO"]

    rich.print(rich.rule.Rule())
    if is_dirty:
        state.append("[bold red]|DIRTY|[/bold red]")

    else:
        state.append("[bold green]|CLEAN|[/bold green]")

    if is_head:
        state.append("[bold yellow]|DETACHED|[/bold yellow]")

    elif is_behind:
        state.append("[bold red]|DESYNC|[/bold red]")

    else:
        state.append("[bold green]|SYNCED|[/bold green]")

    state.append(working_dir)
    rich.print(" ".join(state))
    rich.print(rich.rule.Rule())

    return True

@sos_tool
def repo_commit(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    working_dir: Annotated[str, Field(description="The working directory for the Repo")],
    message: Annotated[Optional[str], Field(description="The message to include with the commit")] = None,
):
    """Commit the working_dir repo to the remote"""
    rich.print({"git.repo_commit":
            {"working_dir":working_dir
             }
        })

    repo = git.Repo(working_dir)

    is_dirty = repo.is_dirty()

    cur_hash = repo.head.object.hexsha
    origin = repo.remotes.origin
    origin.fetch()

    try:
        new_hash = origin.refs[repo.active_branch.name].object.hexsha
        is_behind = cur_hash != new_hash
        is_head = False

    except:
        # TODO
        # - this should only catch the detatched head error not all errors
        is_behind = False
        is_head = True

    rich.print(rich.rule.Rule())
    if is_head:
        rich.print(f"[bold red]REPO IS DETATCHED:[/bold red] {working_dir}")
        rich.print(f"[bold red]NEEDS TO BE MANUALLY FIXED[/bold red]")

    elif is_behind:
        rich.print(f"[bold red]REPO OUT OF SYNC:[/bold red] {working_dir}")
        rich.print(f"[bold red]NEEDS TO BE MANUALLY FIXED[/bold red]")

    elif is_dirty:
        rich.print(f"[bold red]COMMIT FROM:[/bold red] {working_dir}")
        repo.git.add(all=True)
        rich.print(repo.git.status())

        if message is None and __CTX__.meta.input_method == "CLI":
            message = input("Commit Message: ")

        elif message is None:
            message = "COMMIT FROM SOS-TOOLKIT"

        #
        # TODO
        # - if not CLI
        # - must provide credentials
        #
        repo.git.commit("-m", message)
        repo.git.push()

    else:
        rich.print(f"[bold green]REPO CLEAN:[/bold green] {working_dir}")
    rich.print(rich.rule.Rule())


    return True


@sos_tool
def repo_fetch(
    working_dir: Annotated[str, Field(description="The working directory for the Repo")],
    raise_exc: Annotated[bool, Field(description="If raise exception on runtime error")] = True
):
    """Fetch updates for a target repo"""

    try:
        git.Repo(working_dir).fetch()

    except Exception as exc:
        if raise_exc:
            raise

        else:
            e = f"[red]::GIT_ERROR::[/red] RUNTIME EXCEPTION: {exc}"
            rich.print(e)

    return True

@sos_tool
def repo_pull(
    working_dir: Annotated[str, Field(description="The working directory for the Repo")],
    raise_exc: Annotated[bool, Field(description="If raise exception on runtime error")] = True
):
    """Pull updates for a target repo"""

    try:
        git.Repo(working_dir).pull()

    except Exception as exc:
        if raise_exc:
            raise

        else:
            e = f"[red]::GIT_ERROR::[/red] RUNTIME EXCEPTION: {exc}"
            rich.print(e)

    return True

@sos_tool
def repo_checkout(
    working_dir: Annotated[str, Field(description="The working directory for the Repo")],
    target: Annotated[str, Field(description="The target for checkout")],
    raise_exc: Annotated[bool, Field(description="If raise exception on runtime error")] = True
):
    """Checkout a target git tag/branch"""

    try:
        git.Repo(working_dir).checkout(target)

    except Exception as exc:
        if raise_exc:
            raise

        else:
            e = f"[red]::GIT_ERROR::[/red] RUNTIME EXCEPTION: {exc}"
            rich.print(e)

    return True
