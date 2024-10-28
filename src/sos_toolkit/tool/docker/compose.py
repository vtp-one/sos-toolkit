from typing import Optional, Annotated, Literal, Union, List, Dict
from collections.abc import MutableMapping
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, sos_tool
import tempfile
import rich

from ._client import get_client

@sos_tool
def compose_up(
    __CTX__: Annotated[Optional[SOSContext], Field(description="SOSContext Object")],
    file: Annotated[str, Field(description="The Location of the Compose File")],
    project_name: Annotated[str, Field(description="The Compose Project Name")],
    profile: Annotated[Optional[str], Field(description="The Profile to use from the Compose File")] = None,
    env_map: Annotated[Optional[Dict[str, str]], Field(description="Dict of Values for Compose Env")] = []
):
    """Start a Docker Compose project"""

    rich.print({"docker.compose_up":
            {
            "file":file,
            "profile":profile,
            "project_name":project_name
            }
        })

    docker_args = {}
    docker_args["compose_files"] = [file]
    docker_args["compose_project_name"] = project_name

    if profile:
        docker_args["compose_profiles"] = [profile]

    with tempfile.NamedTemporaryFile() as env_file:
        rich.print(f"COMPOSE_ENV:")
        rich.print(env_map)
        with open(env_file.name, "w") as f:
            for key, value in env_map.items():
                f.write(f"{key}={value}\n")

        docker_args["compose_env_file"] = env_file.name

        docker = get_client(**docker_args)

        compose_args = {}
        compose_args["detach"] = True
        compose_args["wait"] = True
        compose_args["no_build"] = True

        docker.compose.up(**compose_args)

    return {
            "file":file,
            "profile":profile,
            "project_name":project_name
            }


@sos_tool
def compose_down(
    project_name: Annotated[str, Field(description="The Compose Project Name")],
    profile: Annotated[Optional[str], Field(description="The profile to use from the compose file")] = None
):
    """Stop a Docker Compose Project"""
    rich.print({"docker.compose_down":
            {
            "project_name":project_name,
            "profile":profile,
            }
        })

    docker_args = {}
    docker_args["compose_project_name"] = project_name

    if profile:
        docker_args["compose_profiles"] = [profile]

    docker = get_client(**docker_args)

    compose_args = {}

    #
    # TODO:
    #
    #kwargs = ["services", "remove_orphans", "remove_images", "timeout", "volumes", "quiet"]

    docker.compose.down(**compose_args)

    return True