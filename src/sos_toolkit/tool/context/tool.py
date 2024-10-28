from typing import Optional, Annotated, Any, Dict, Literal, Callable
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, ResultObject, sos_tool, ToolRepo, ToolObject

import rich

from os import listdir
from os.path import isdir, isfile, basename, abspath, dirname, join
from pathlib import Path
import importlib.util
import sys

@sos_tool
def tool_remove(
    namespace: Annotated[str, Field(description="ToolRepo namespace for the tool")],
    key: Annotated[str, Field(description="Key for the tool")]
):
    """Remove a Tool"""
    rich.print({"context.tool_remove":
            {
            "namespace":namespace,
            "key":key
            }
        })

    if not isinstance((repo := SOS_TOOL.get(namespace, None)), ToolRepo):
        e = f"INVALID NAMESPACE: {namespace}"
        raise RuntimeError(e)

    if not hasattr(repo, key):
        e = f"INVALID KEY: {namespace} - {key}"
        raise RuntimeError(e)

    delattr(repo, key)

    return True


@sos_tool
def tool_string(
    code: Annotated[str, Field(description="Python Code String for tool")],
    namespace: Annotated[str, Field(description="ToolRepo namespace for the tool")],
    key: Annotated[str, Field(description="Key for the tool")],
    meta: Annotated[Optional[Dict], Field(description="MetaData for tool")] = {},
    description: Annotated[Optional[str], Field(description="Description for tool")] = None,
    overwrite: Annotated[Optional[bool], Field(description="If overwrite preexisting tool")] = False,
    validate: Annotated[Optional[bool], Field(description="If validate function")] = True
):
    """Register a tool from a string of python code"""
    # this is not a very good idea
    # but would be fun
    raise NotImplementedError()

    pass


@sos_tool
def tool_function(
    function: Annotated[Callable, Field(description="Target function for tool")],
    namespace: Annotated[str, Field(description="ToolRepo namespace for the tool")],
    key: Annotated[str, Field(description="Key for the tool")],
    meta: Annotated[Optional[Dict], Field(description="MetaData for tool")] = {},
    description: Annotated[Optional[str], Field(description="Description for tool")] = None,
    overwrite: Annotated[Optional[bool], Field(description="If overwrite preexisting tool")] = False,
    validate: Annotated[Optional[bool], Field(description="If validate function")] = True
):
    """Register a Tool from a Function"""

    rich.print({"context.tool_function":
            {
            "namespace":namespace,
            "key":key,
            "function":function,
            "meta":meta,
            "description":description,
            "overwrite":overwrite,
            }
        })

    SOS_TOOL.register(
        function=function,
        namespace=namespace,
        key=key,
        meta=meta,
        description=description,
        overwrite=overwrite,
        validate=validate)

    return  {
            "namespace":namespace,
            "key":key,
            "function":function,
            "meta":meta,
            "description":description,
            "overwrite":overwrite,
            "tool_target":".".join([namespace, key]),
            }


@sos_tool
def tool_file(
    namespace: Annotated[str, Field(description="ToolRepo namespace for the tools")],
    file: Annotated[str, Field(description="Target file to load tools")],
    overwrite: Annotated[Optional[bool], Field(description="If overwrite preexisting tool")] = False
):
    """Register tools from a file"""
    raise NotImplementedError()
    #
    # TODO
    # - need a way to parse the namespace into the loaded file
    # - not sure how this would be possible
    # - file loading works => it just pulls the parent directory as the namespace
    #   from the decorator
    # - if we directly load the tool and skip the SOS_TOOL loader entirely
    #   it would work
    # - maybe just patch the tool loader before loading the file?
    # - how can we make the file use a different version of sos_tool
    #
    rich.print({"context.tool_file":
            {
            "namespace":namespace,
            "file":file,
            "overwrite":overwrite,
            }
        })


@sos_tool
def tool_module(
    target: Annotated[str, Field(description="Target module to load tools")],
    overwrite: Annotated[Optional[bool], Field(description="If overwrite preexisting tool")] = False
):
    """Register tools from a module"""
    rich.print({"context.tool_module":
            {
            "target": target,
            "overwrite":overwrite,
            }
        })

    # TODO
    # - CHECK THE MODULE IS VALID

    # get file list
    file_list = [join(target, f) for f in listdir(target) if basename(f).endswith(".py") and not basename(f).startswith("_")]

    rich.print(file_list)

    output = []
    for module in file_list:

        module_file = Path(module).resolve()
        namespace = module_file.parent.name
        _module = module_file.name[:-3]
        module_name = f"{namespace}.{_module}"

        rich.print(module_file)
        spec = importlib.util.spec_from_file_location(module_name, module_file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        output.append({"module":module, "module_file":module_file, "namespace":namespace, "module_name":module_name})

    return output
