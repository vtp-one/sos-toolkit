from typing import Optional, Annotated, Callable
from pydantic import Field
import rich

from IPython.terminal.embed import InteractiveShellEmbed

import sos_toolkit
from sos_toolkit.meta import SOSContext, sos_action, ResultRepo

@sos_action
def cli(
    context_file: Annotated[Optional[str], Field(description="The target context_file")] = "",
    save_on_exit: Annotated[bool, Field(description="If save context on exit")] = True
):

    """Open an IPython console in an SOSContext"""
    rich.print({"SOS_CLI":
            {
            "context_file":context_file,
            "save_on_exit":save_on_exit
            }
        })

    try:
        __CTX__ = SOSContext.file_load(context_file=context_file)

    except FileNotFoundError:
        rich.print(f"NO CONTEXT_FILE FOUND - USING ROOT CONTEXT")
        __CTX__ = SOSContext.generate(system_file=False)
        save_on_exit = False

    result = __CTX__.run("action.sos_cli")

    save_on_exit = str(save_on_exit).ljust(5, " ")

    banner = "\n".join([
        "*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*",
        "*SOS*                               *SOS*",
        "*SOS*     SOS-TOOLKIT CLI ENTER     *SOS*",
        "*SOS*    CURRENT CONTEXT: __CTX__   *SOS*",
        "*SOS*   TO EXIT CONSOLE USE: exit   *SOS*",
       f"*SOS*   ON EXIT SAVE __CTX__: {save_on_exit} *SOS*",
        "*SOS*                               *SOS*",
        "*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*",
        ])
    exit = "\n".join([
         "*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*",
         "*SOS*                               *SOS*",
         "*SOS*     SOS-TOOLKIT CLI EXIT      *SOS*",
        f"*SOS*   ON EXIT SAVE __CTX__: {save_on_exit} *SOS*",
         "*SOS*                               *SOS*",
         "*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*"
        ])

    InteractiveShellEmbed(banner1=banner, exit_msg=exit)()

    if save_on_exit:
        __CTX__.file_save()

    return result
