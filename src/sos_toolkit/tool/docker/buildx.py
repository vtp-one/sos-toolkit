from typing import Union, Optional, Annotated, Literal, List, Dict
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, sos_tool
import rich

from copy import deepcopy
from requests import get as requests_get
from os.path import exists as path_exists
from os.path import join as path_join


from ._client import get_client

#
# TODO
# - if cache bust fails on no network but image exists => use preexisting image
# - how to do that for bake?
# - need to check all the targets? is that even possible?
# - would need to parse the hcl file probably
# - or maybe use the buildx.print to get the image tags?
# - would not work if one cache fails but isn't needed for the missing image
# - would need to be able to map cache targets to image targets
#
# TODO
# - add reserved image tags to prevent overwriting sos-namespace images
#

def _cache_bust(
    kind: Annotated[Literal["gitea"], Field(description="Kind of Remote")],
    target: Annotated[str, Field(description="Remote Target")],
    verify_ssl: Annotated[bool, Field(description="If verify SSL certificate for remote request")] = True
):

    match kind:
        case "gitea":
            r = requests_get(target, verify=verify_ssl)
            result = r.json()[0]["sha"]

        case "github":
            raise NotImplementedError()

        case "gitlab":
            raise NotImplementedError()

        case _:
            raise RuntimeError()

    return result

@sos_tool
def buildx_bake(
    __CTX__: Annotated[Optional[SOSContext], Field(description="SOSContext Object")],
    bake_file: Annotated[str, Field(description="The name of the bake_file to use")],
    bake_target: Annotated[str, Field(description="The target to use from the bake_file")],
    namespace: Annotated[str, Field(description="The namespace of the output containers")],
    context_dir: Annotated[str, Field(description="The root directory to use for the build")],
    version: Annotated[Optional[str], Field(description="The version variable to use")] = None,
    platform: Annotated[Optional[str], Field(description="The platform variable to use")] = None,
    variables: Annotated[Optional[Dict], Field(description="Variables to pass to the build")] = {},
    cache_bust: Annotated[Optional[Dict], Field(description="Key-Value pairs to use for Cache Bust")] = {},
    client_config: Annotated[Optional[Dict], Field(description="The Docker Client Config dict")] = {},
    print_bakex: Annotated[Optional[bool], Field(description="If print bakex build before running")] = True
):
    """Use Docker Buildx bake to build containers"""

    rich.print({"docker.buildx_bake":
            {
                "bake_file":bake_file,
                "bake_target":bake_target,
                "namespace":namespace,
                "context_dir":context_dir,
                "variables":variables,
                "cache_bust":cache_bust,
                "client_config":client_config,
                "print_bakex":print_bakex
            }
        })

    variables = deepcopy(variables)
    docker = get_client(**client_config)

    if not path_exists(context_dir):
        e = f"CONTEXT_DIR NOT FOUND: {context_dir}"
        raise RuntimeError(e)

    bake_file = path_join(context_dir, bake_file)

    if not path_exists(bake_file):
        e = f"BAKEFILE NOT FOUND: {bake_file}"
        raise RuntimeError(e)

    variables["CONTEXT_ROOT"] = context_dir
    variables["NAMESPACE"] = namespace
    variables["VERSION"] = version or "0.0.0" if __CTX__ is None else __CTX__.meta.system_version
    variables["PLATFORM"] = platform or __CTX__.meta.platform

    # TODO
    # - validate additional context
    # - what validation do they need?
    # for c in additional_context:
    # validate(c)

    bust = {}
    for key, target in cache_bust.items():
        bust[f"CACHE_BUST_{key}".upper()] = _cache_bust(**target)

    variables.update(bust)

    buildx_args = {}
    buildx_args["files"] = [bake_file]
    buildx_args["targets"] = [bake_target]
    buildx_args["variables"] = variables

    rich.print({"docker.buildx_bake.buildx_args":buildx_args})

    if print_bakex:
        rich.print({"docker.buildx_bake.print_bakex":docker.buildx.bake(print=True, **buildx_args)})

    try:
        docker.buildx.bake(**buildx_args)
        success = True

    except Exception as exc:
        e = f"DOCKER BAKEX EXC - {exc}"
        success = False

    if not success:
        raise RuntimeError(e)

    #
    # TODO
    # - streaming response
    #

    return {
            "bake_file":bake_file,
            "bake_target":bake_target,
            "namespace":namespace,
            "context_dir":context_dir,
            "variables":variables,
            "cache_bust":cache_bust,
            "client_config":client_config,
            }

@sos_tool
def buildx_build(
    __CTX__: Annotated[Optional[SOSContext], Field(description="SOSContext Object")],
    docker_file: Annotated[str, Field(description="The name of the docker file to use")],
    context_dir: Annotated[str, Field(description="The path of the context to use")],
    tags: Annotated[Union[str, List[str]], Field(description="The tags for the built image")],
    platform: Annotated[Optional[str], Field(description="The platform variable to use")] = None,
    version: Annotated[Optional[str], Field(description="The version for the image")] = None,
    build_args: Annotated[Optional[Dict[str, str]], Field(description="Dictionary of build args")] = {},
    build_target: Annotated[Optional[str], Field(description="The build target")] = None,
    client_config: Annotated[Optional[Dict], Field(description="Docker Client config dict")] = {},
    build_kwargs: Annotated[Optional[Dict], Field(description="Additional kwargs to pass to the build")] = {},
    cache_bust: Annotated[Optional[Dict], Field(description="Key-Value pairs to use for Cache Bust")] = {},
):
    """Build an image from a docker file"""

    rich.print({"docker.buildx_build":
            {
            "docker_file":docker_file,
            "context_dir":context_dir,
            "tags":tags,
            "platform":platform,
            "build_args":build_args,
            "build_target":build_target,
            "client_config":client_config,
            "build_kwargs":build_kwargs,
            "cache_bust":cache_bust,
            }
        })

    variables = deepcopy(build_args)
    docker = get_client(**client_config)

    if not path_exists(context_dir):
        e = f"CONTEXT_DIR NOT FOUND: {context_dir}"
        raise RuntimeError(e)

    _docker_file = path_join(context_dir, docker_file)

    if not path_exists(_docker_file):
        e = f"DOCKERFILE NOT FOUND: {_docker_file}"
        raise RuntimeError(e)

    variables["VERSION"] = version or "0.0.0" if __CTX__ is None else __CTX__.meta.system_version
    variables["PLATFORM"] = platform or __CTX__.meta.platform

    bust = {}
    for key, target in cache_bust.items():
        bust[f"CACHE_BUST_{key}".upper()] = _cache_bust(**target)

    variables.update(bust)

    _tags = tags if isinstance(tags, list) else [tags]

    build_kwargs["context_path"] = context_dir
    build_kwargs["file"] = _docker_file
    build_kwargs["tags"] = _tags

    if build_target and "target" not in build_kwargs:
        build_kwargs["target"] = build_target

    build_kwargs["build_args"] = variables

    rich.print({"docker.buildx_build.build_kwargs":build_kwargs})

    result = docker.build(**build_kwargs)

    return {
            "docker_file":docker_file,
            "context_dir":context_dir,
            "tags":tags,
            "build_kwargs":build_kwargs
            }
