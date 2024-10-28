from typing import Optional, Annotated, Callable
from pydantic import Field
import rich

from os.path import exists as path_exists

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def setup(
    system_file: Annotated[Optional[str], Field(description="The target system file")] = "",
    local_file: Annotated[Optional[str], Field(description="The target local file")] = "",
    user_file: Annotated[Optional[str], Field(description="The target user file")] = "",
    root_file: Annotated[Optional[str], Field(description="The target root file")] = "",
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
    overwrite: Annotated[Optional[bool], Field(description="If overwrite pre-existing context_file")] = False,
    installed: Annotated[Optional[bool], Field(description="If set is_installed")] = False,
    profile: Annotated[Optional[str], Field(description="The target profile to enable")] = "",
    persist: Annotated[Optional[bool], Field(description="If persist pre-existing context values")] = False,
    ignore_version: Annotated[Optional[bool], Field(description="If Ignore SOS-Toolkit Version Mismatch")] = False,
    test: Annotated[Optional[bool], Field(description="If test generate context for errors without saving")] = False,
    run_setup: Annotated[Optional[bool], Field(description="If run sos_setup from generated context")] = True,
):

    """Generate the System SOSContext"""
    rich.print({"SOS_SETUP":
            {
            "system_file":system_file,
            "local_file":local_file,
            "user_file":user_file,
            "root_file":root_file,
            "context_file":context_file,
            "overwrite":overwrite,
            "installed":installed,
            "profile":profile,
            "persist":persist,
            "ignore_version":ignore_version,
            "test":test,
            "run_setup":run_setup
            }
        })

    __CTX__ = SOSContext.generate(
        system_file=system_file,
        local_file=local_file,
        user_file=user_file,
        root_file=root_file,
        context_file=context_file,
        persist=persist,
        ignore_version=ignore_version)

    if test:
        rich.print(__CTX__)
        result = ResultRepo(__CTX__=__CTX__)

    else:
        if not overwrite and path_exists(__CTX__.meta.context_file):
            e = f"TARGET CONTEXT_FILE EXISTS AND NOT OVERWRITE: {__CTX__.meta.context_file}"
            raise RuntimeError(e)

        __CTX__.run("hook.on_context_load")

        if run_setup:
            result = __CTX__.run("action.sos_setup")

        else:
            result = ResultRepo()

        if profile != "":
            __CTX__.meta.profile = profile

        __CTX__.meta.is_installed = installed
        __CTX__.file_save(run_hooks=False)

        result.set("__CTX__", __CTX__)

    return result
