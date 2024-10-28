from typing import Optional, Annotated
from pydantic import Field
import rich

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def update(
    system_file: Annotated[Optional[str], Field(description="The target system file")] = "",
    local_file: Annotated[Optional[str], Field(description="The target local file")] = "",
    user_file: Annotated[Optional[str], Field(description="The target user file")] = "",
    root_file: Annotated[Optional[str], Field(description="The target root file")] = "",
    persist: Annotated[Optional[bool], Field(description="If persist pre-existing context values")] = False,
    ignore_version: Annotated[Optional[bool], Field(description="If Ignore SOS-Toolkit Version Mismatch")] = False,
    context_file: Annotated[Optional[str], Field(description="The old context_file")] = "",
    target: Annotated[Optional[str], Field(description="The context object for update")] = None,
    action_update: Annotated[Optional[str], Field(description="If run action sos_update")] = True
):

    """Update a System SOSContext"""
    rich.print({"SOS_UPDATE":
            {
            "system_file":system_file,
            "local_file":local_file,
            "user_file":user_file,
            "root_file":root_file,
            "persist":persist,
            "ignore_version":ignore_version,
            "context_file":context_file,
            "target":target,
            }
        })

    if target.startswith("namespace"):
        e = f"CAN NOT UPDATE NAMESPACE VALUE - USE CONTEXT --SET-VALUE INSTEAD - target: {target}"
        raise RuntimeError(e)

    __OLD_CTX__ = SOSContext.file_load(context_file=context_file)

    __NEW_CTX__ = SOSContext.generate(
        system_file=system_file,
        local_file=local_file,
        user_file=user_file,
        root_file=root_file,
        context_file=None,
        persist=False,
        runtime_config={"namespace":__OLD_CTX__.namespace.dict()},
        ignore_version=ignore_version)

    obj = __NEW_CTX__.get(target)
    __OLD_CTX__.set(target, obj, True)

    if action_update:
        __OLD_CTX__.run("hooks.on_context_load")
        result = __OLD_CTX__.run("action.sos_update")

    else:
        result = ResultRepo(__CTX__=__OLD_CTX__)

    __OLD_CTX__.file_save()
    return result
