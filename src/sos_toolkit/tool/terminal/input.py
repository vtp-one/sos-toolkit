from typing import Optional, Annotated, Any, List
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, ResultObject, sos_tool

import rich

@sos_tool
def input_prompt(
    prompt: Annotated[str, Field(description="Prompt for the input")],
    default: Annotated[str, Field(description="Default value for input")] = "",
    valid: Annotated[Optional[List[str]], Field(description="Valid Input Values")] = []
):
    """Get Input from a CLI Prompt"""

    rich.print({"terminal.input_prompt":
            {
            "prompt":prompt,
            "default":default,
            "valid":valid,
             }
        })

    if default == "":
        default = None

    while True:
        #
        # TODO:
        # - how to break out of here?
        #
        rich.print(prompt)
        if default:
            rich.print(f"DEFAULT: {default}")

        if len(valid):
            rich.print(f"VALID: {valid}")

        obj = input()

        if obj == "":
            obj = default

        if obj is None:
            rich.print(f"NO INPUT PROVIDED AND NO DEFAULT")

        else:
            if len(valid):
                if obj in valid:
                    break

                else:
                    rich.print(f"INPUT INVALID: {obj}")

            else:
                break

    return {"input":obj}
