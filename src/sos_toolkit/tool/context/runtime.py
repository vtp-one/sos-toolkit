from typing import Optional, Annotated, Any, Dict, List, Union, Literal
from pydantic import Field
from sos_toolkit.meta import (
    SOSContext,
    sos_tool,
    MetaRunnable,
    MetaObject,
    MetaConfig,
    MetaCondition,
    RuntimeBreak,
    ResultRepo,
    _global
    )

import rich
from omegaconf import OmegaConf
from os import environ


@sos_tool
def runtime_object(
    target: Annotated[str, Field(description="Target to run")],
    context: Annotated[Optional[SOSContext], Field(description="SOSContext object")] = None,
    context_file: Annotated[Optional[str], Field(description="Target SOSContext file")] = None,
    params: Annotated[dict, Field(description="Paramaters for the Action")] = {},
    save_context: Annotated[bool, Field(description="If save SOSContext after run")] = True,
):
    """Run a target object from a context"""

    rich.print({"context.runtime_object":
            {
            "target":target,
            "context":context,
            "context_file":context_file,
            "params":params,
            "save_context":save_context,
             }
        })

    if context is None and context_file is None:
        e = f"MUST PROVIDE EITHER CONTEXT OR CONTEXT_FILE - target: {target}"
        raise RuntimeError(e)

    __CTX__ = context or SOSContext.file_load(context_file=context_file)

    #
    # TODO
    # - pipe params into run / context somehow?
    # - just update the context?
    # - need to refactor runnable to do this correctly
    #
    for key, value in params:
        __CTX__.set(key, value)

    result = __CTX__.run(_target)

    if save_context:
        __CTX__.file_save()

    return result

@sos_tool
def runtime_nested(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    target: Annotated[str, Field(description="Target to run")],
    params: Annotated[dict, Field(description="Paramaters for the Action")] = {},
):
    """Run a target object from the provided context"""
    rich.print({"context.runtime_nested":
            {
            "target":target,
            "params":params,
             }
        })
    for key, value in params:
        __CTX__.set(key, value)

    return __CTX__.run(target)

@sos_tool
def runtime_breakpoint(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    label: Annotated[str, Field(description="Label for the breakpoint")],
):
    """Create a Breakpoint"""
    rich.print({"context.runtime_breakpoint":
            {
            "label":label
             }
        })

    breakpoint()

    return True

@sos_tool
def runtime_exception(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    exc: Annotated[Optional[Any], Field(description="Exception Object to Raise")] = None,
    exc_data: Annotated[Optional[str], Field(description="Exception Data to Create Exception")] = None,
    exc_kind: Annotated[Optional[Literal["not_implemented", "runtime", "value", "type", "break"]], Field(description="Exception Kind to Create Exception")] = None,
):
    """Raise An Exception"""
    rich.print({"context.runtime_exception":
            {
            "exc":exc,
            "exc_data":exc_data,
            "exc_kind":exc_kind,
            }
        })


    if exc:
        raise Exc

    else:
        match exc_kind:
            case "not_implemented":
                raise NotImplementedError(exc_data)

            case "runtime":
                raise RuntimeError(exc_data)

            case "value":
                raise ValueError(exc_data)

            case "type":
                raise TypeError(exc_data)

            case "break":
                raise RuntimeBreak(exc_data)

            case _:
                e = f"INVALID EXCEPTION KIND - {exc_kind} - {exc_data}"
                raise RuntimeError(e)

    return False

@sos_tool
def runtime_match(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    match_value: Annotated[str, Field(description="The Value to Match")],
    match_map: Annotated[dict, Field(description="The Mapping of Values to Actions")],
):
    """Run an Action By Matching Value to Map"""

    # only works for string based matches => no support for resolveable / conditions
    rich.print({"context.runtime_match":
            {
            "match_value":match_value
            }
        })


    obj = match_map.get(match_value, None)

    match obj:
        case None:
            e = f"INVALID MATCH_VALUE - {match_value} - valid: {match_map.keys()}"
            raise RuntimeError(e)

        case MutableMapping():
            if "tool" in obj.keys():
                obj = MetaRunnable(**obj)

            else:
                obj = MetaObject(**obj)

            result = obj(__CTX__)

        case MetaRunnable() | MetaObject() | MetaConfig():
            result = obj(__CTX__)

        case _:
            result = obj

    return result


@sos_tool
def runtime_local(
    obj: Annotated[dict, Field(description="Object to write to Local")],
    file: Annotated[Optional[str], Field(description="Target file to write to")] = None,
):
    """Write a value to an sos-local.yaml file"""

    rich.print({"context.runtime_local":
            {
            "obj":obj,
            "file":file
            }
        })

    if _file is not None:
        SOSContext.generate(
            system_file=False,
            local_file=file,
            user_file=False,
            root_file=False)

        _file = OmegaConf.load(_file)

    else:
        _file = OmegaConf.create({})

    obj = OmegaConf.create(obj)
    obj = OmegaConf.merge(_file, obj)

    if file is None:
        file = environ.get(_global.ENV_LOCAL_FILE, _global.LOCAL_FILE)

    OmegaConf.save(obj, file)

    return file

@sos_tool
def runtime_break(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    info_pass: Annotated[Optional[str], Field(description="Output Text if Pass")] = None,
    info_break: Annotated[Optional[str], Field(description="Output Text if Break")] = None,
    resolve: Annotated[Optional[List[MetaCondition]], Field(description="List of Condition Objects")] = [],
    qualifier: Annotated[Literal["any", "all", "none"], Field(description="Qualifier for condition objects")] = "all",
    raise_exc: Annotated[bool, Field(description="If raise_exc")] = False
):
    """If all conditions pass break out of current running action"""

    rich.print({"context.runtime_break":
            {
            "info_pass":info_pass,
            "info_break":info_break
            }
        })

    _resolve = []

    if len(resolve):
        for _res in resolve:
            if not isinstance(_res, MetaCondition):
                _res = MetaCondition(**_res)

            _resolve.append(_res.resolve(__CTX__, raise_exc=False))

        match qualifier:
            case "any":
                _qualifier = any(_resolve)

            case "all":
                _qualifier = all(_resolve)

            case "none":
                _qualifier = not all(_resolve)

            case _:
                e = f"INVALID QUALIFIER - {qualifier}"
                raise RuntimeError(e)

        if _qualifier:
            if info_break:
                rich.print(f"RUNTIME_BREAK - BREAK - {info_break}")

            raise RuntimeBreak(info_break, data=_resolve)

        else:
            if raise_exc:
                e = f"RUNTIME_BREAK - RESOLVE FAILED - {info_break}"
                raise RuntimeError(e)

            else:
                if info_pass:
                    rich.print(f"RUNTIME_BREAK - PASS - {info_pass}")

    else:
        raise RuntimeBreak(info_break, data=_resolve)

    return ResultRepo(resolve=_resolve, info=info_pass, qualifier=_qualifier)
