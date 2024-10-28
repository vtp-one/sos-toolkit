from typing import Optional, Annotated, Any, Dict, List, Union, Literal
from pydantic import Field
from sos_toolkit.meta import SOSContext, SOS_TOOL, ResultObject, sos_tool, MetaCondition

import rich

@sos_tool
def ctx_parse(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    targets: Annotated[Dict[str,Union[str, List, Dict]], Field(description="Key-Value Pairs to map From Context To Result")],
):
    """Build a dictionary from key-value pairs parsed form SOSContext"""
    rich.print({"context.ctx_parse":
            {"targets":targets
             }
        })
    output = {}
    for key, obj in targets.items():
        output[key] = __CTX__.get(obj)

    return {"output":output}


@sos_tool
def ctx_format(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    format_string: Annotated[str, Field(description="F-String to parse")],
    input_values: Annotated[Dict[str, str], Field(description="Key-Value Pairs to pass to the formater")] = {},
    ctx_targets: Annotated[Dict[str, Union[str, List, Dict]], Field(description="Key-Value Pairs to extract from Context")] = {},
):
    """Build a F-String output by passing Key-Value Pair Input Values and Key-Value Pair SOSContext Targets"""
    rich.print({"context.ctx_format":
            {"format_string":format_string,
             "input_values":input_values,
             "ctx_targets":ctx_targets
             }
        })
    for key, obj in ctx_targets.items():
        input_values[key] = __CTX__.get(obj)

    return {"output":format_string.format(**input_values)}


@sos_tool
def ctx_resolve(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")]
):
    """Resolve variables using an OmegaConf dict and update the SOSContext with the resolved config"""
    rich.print({"context.ctx_resolve":True})
    raise NotImplementedError()
    #
    # TODO
    # - is this recursive? => resolve resolving resolves
    # - what should this do (if anything?)
    # - provide new OmegaConf object => then resolve?
    # - this would then work similar to a merge?
    # - then we could use OmegaConf.merge
    # - does that do anything useful?
    #
    config = OmegaConf(__CTX__.dict())
    OmegaConf.resolve(ctx)
    new_ctx = SOSContext.from_config(config)

    for key in new_ctx.__fields__():
        setattr(__CTX__, key, value)

    return True


@sos_tool
def ctx_flag(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    condition: Annotated[List[MetaCondition], Field(description="List of Condition Objects that must be True")],
    raise_exc: Annotated[Optional[bool], Field(description="Raise an Excpetion if a Condition Fails")] = None,
    return_list: Annotated[bool, Field(description="Return a list of Condition Resolve Results")] = False,
):
    """Evaluate Condition Objects"""
    rich.print({"context.ctx_flag":
            {"condition":condition,
             "raise_exc":raise_exc,
             "return_list":return_list
             }
        })
    result = []
    if raise_exc is not None:
        for cond in condition:
            if not isinstance(cond, MetaCondition):
                cond = MetaCondition(**cond)
            result.append(cond.resolve(context=__CTX__, raise_exc=raise_exc))

    else:
        for cond in condition:
            if not isinstance(cond, MetaCondition):
                cond = MetaCondition(**cond)
            result.append(cond.resolve(context=__CTX__))

    if return_list:
        return result

    else:
        return all(result)


@sos_tool
def ctx_set(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    obj: Annotated[Any, Field(description="Object to insert in SOSContext.namespace")],
    ctx_key: Annotated[str, Field(description="Dot Notation Key of the Object in the SOSContext.namespace")],
    overwrite: Annotated[bool, Field(description="If overwrite key")] = False,
):
    """Set an Object in an SOSContext.namespace"""
    rich.print({"context.ctx_set":
            {
            "obj":obj,
            "ctx_key":ctx_key,
            "overwrite":overwrite
            }
        })

    __CTX__.set(name=ctx_key, value=obj, overwrite=overwrite)

    return {"ctx_key":ctx_key, "obj":obj}


@sos_tool
def ctx_remove(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    ctx_key: Annotated[str, Field(description="Dot Notation Key of the Object in the SOSContext.namespace")],
):
    """Remove an object from an SOSContext.namespace"""
    rich.print({"context.ctx_remove":
            {
            "ctx_key":ctx_key,
            }
        })

    __CTX__.remove(name=ctx_key)

    return True


@sos_tool
def ctx_has(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    parent: Annotated[str, Field(description="Parent object for lookup")],
    target: Annotated[Union[str, List[str]], Field(description="Target object for lookup")],
    raise_exc: Annotated[bool, Field(description="If raise exception on missing target")] = False,
    qualifier: Annotated[Literal["any", "all", "none"], Field(description="Qualifier used")] = "all"
):
    """Returns True if target is a child object of parent"""
    rich.print({"context.ctx_has":
            {
            "parent":parent,
            "target":target,
            "raise_exc":raise_exc,
            "qualifier":qualifier,
            }
        })

    obj = __CTX__.get(parent)

    if not isinstance(target, list):
        _target = [target]

    else:
        _target = target

    result = [obj.has(t) for t in _target]

    match qualifier:
        case "any":
            result = any(*result)

        case "all":
            result = all(*result)

        case "none":
            result = not all(*result)

        case _:
            e = f"INVALID QUALIFIER: {qualifier}"
            raise RuntimeError(e)

    if raise_exc and not result:
        e = f"QUALIFIER FAILED: qualifier: {qualifier} - parent: {parent} - target: {target}"
        raise ValueError(e)

    return {"result":result}


@sos_tool
def ctx_get(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    target: Annotated[str, Field(description="Target Object")]
):
    """Get an Object in an SOSContext"""
    rich.print({"context.ctx_get":
            {
            "target":target
            }
        })

    obj = __CTX__.get(target)

    return {"obj":obj}


@sos_tool
def ctx_merge(
    __CTX__: Annotated[SOSContext, Field(description="SOSContext Object")],
    system_file: Annotated[str, Field(description="Target System File to merge into SOSContenxt")]
):
    """Merge a Target system file into the current system context"""

    new_config = SOSContext.generate(
        system_file=system_file,
        local_file=__CTX__.meta.local_file,
        user_file=__CTX__.meta.user_file,
        root_file=__CTX__.meta.root_file).dict()

    old_config = __CTX__.dict()

    config = OmegaConf.merge(old_config, new_config)

    new_ctx = SOSContext.from_config(config)

    for key in __CTX__.model_fields.keys():
        value = new_ctx.get(key)
        __CTX__._set(key, value, overwrite=True, force=True)

    return True
