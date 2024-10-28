from typing import Optional, Annotated, Any, Union, List
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, ResultObject, sos_tool

import rich
import tqdm
import ollama

#
# TODO
# - make model repository ops not require container being loaded
#

@sos_tool
def debug(
):
    """Test Plugin for Service Installations"""

    rich.print({"ollama.debug":True})

    return True

@sos_tool
def download_models(
    target: Annotated[Union[str, List[str]], Field(description="Target models to download from Ollama Library")],
    client_kwargs: Annotated[Optional[dict], Field(description="Kwargs for the Ollama Client")] = {}
):
    """Download an Ollama Model to local_data"""
    rich.print({"ollama.download_model":
            {
            "target":target,
            "client_kwargs":client_kwargs
            }
        })

    if not isinstance(target, list):
        target = [target]

    # call ollama api
    client = ollama.Client(**client_kwargs)
    models = client.list()["models"] or []
    models = [z["name"] for z in models]
    for _target in target:
        if _target not in models:
            rich.print(f"OLLAMA PULLING TARGET: {_target}")

            current_digest, bars = "", {}
            for progress in ollama.pull(_target, stream=True):
              digest = progress.get("digest", "")
              if digest != current_digest and current_digest in bars:
                bars[current_digest].close()

              if not digest:
                print(progress.get("status"))
                continue

              if digest not in bars and (total := progress.get("total")):
                bars[digest] = tqdm.tqdm(total=total, desc=f"pulling {digest[7:19]}", unit="B", unit_scale=True)

              if completed := progress.get("completed"):
                bars[digest].update(completed - bars[digest].n)

              current_digest = digest

        else:
            rich.print(f"OLLAMA TARGET EXISTS: {_target}")

    return True


@ sos_tool
def ollama_api(
    action: Annotated[str, Field(description="Target Method to Use")],
    action_kwargs: Annotated[dict, Field(description="Kwargs for the action")] = {},
    client_kwargs: Annotated[dict, Field(description="Kwargs for the client")] = {}
):
    """Generate an Ollama API Call"""

    rich.print({"ollama.ollama_api":
            {
            "action":action,
            "action_kwargs":action_kwargs,
            "client_kwargs":client_kwargs,
            }
        })

    if action.startswith("_"):
        e = f"INVALID ACTION: {action}"
        raise RuntimeError(e)

    client = ollama.Client(**client_kwargs)
    action = getattr(client, action)
    result = action(**action_kwargs)

    return {"result":result}
