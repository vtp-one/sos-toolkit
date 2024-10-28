###
#
from typing import Literal, List, Dict, Annotated, Optional
import collections.abc
from pydantic import BaseModel, Field

import rich
import os

#
###

###
#
def _dict(obj):
    return isinstance(obj, collections.abc.MutableMapping)

def _list(obj):
    return isinstance(obj, collections.abc.Sequence) and not isinstance(obj, str)

def _parse_rec(obj):
    if _dict(obj):
        return True

    elif _list(obj):
        return True

    else:
        return False

def parse_replace(obj, target, replacement):
    if _dict(obj):
        for key, value in obj.items():
            if _parse_rec(value):
                obj[key] = parse_replace(value, target, replacement)

            elif value == target:
                obj[key] = replacement

    elif _list(obj):
        for (n, value) in enumerate(obj):
            if _parse_rec(value):
                obj[n] = parse_replace(value, target, replacement)

            elif value == target:
                obj[n] = replacement


    elif obj == target:
        obj = replacement

    return obj

###
#
def valid_path(target: Annotated[str, Field(description="Target file to check")]):
    try:
        return os.path.exists(target) and os.path.isfile(target)

    except:
        return False


#
###

###
#
def valid_keys(x, force_string=True, allow_idx=False):
    #if hasattr(x, "keys"):
    if callable((x_k := getattr(x, "keys", None))):
        for key in x_k():
            valid_keys(key)

    elif isinstance(x, str):
        e = f"INVALID KEY: {x}"
        if allow_idx and x.endswith("]"):
            z = x.split("[")
            if len(z) != 2 or not z[0].isidentifier():
                raise RuntimeError(e)

            try:
                int(z[-1].rstrip("]"))

            except:
                raise RuntimeError(e)

        elif not x.isidentifier():
            raise RuntimeError(e)

    elif force_string:
        e = f"INVALID TYPE FOR KEYS: {type(x)} - {x}"
        raise TypeError(e)

    else:
        #rich.print(f"VALID_KEYS GUARD CLAUSE: {type(x)}")
        pass

    return x

def is_idx(x):
    if not x.endswith("]"):
        return False

    z = x.split("[")
    if not len(z) == 2:
        return False

    try:
        int(z[-1].rstrip("]"))
        return True

    except:
        return False

def parse_idx(x):
    _obj, _idx = x.split("[")
    _idx = int(_idx.rstrip("]"))
    return _obj, _idx



#
###


###
#
from pydantic import ConfigDict, validate_call
class CallConfig(ConfigDict):
    validate_assignment = True
    strict = True

def sos_call(func):
    return validate_call(func, config=CallConfig())


#
###


###
#
# debug console
# __import__("sos_toolkit").ipython_portal()
#
from IPython.terminal.embed import InteractiveShellEmbed

def ipython_portal(enter_msg=None, exit_msg=None):
    _enter = "\n".join([
        "*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*",
        "*SOS*                               *SOS*",
        "*SOS*     SOS-TOOLKIT CLI ENTER     *SOS*",
        "*SOS*   TO EXIT CONSOLE USE: exit   *SOS*",
        "*SOS*                               *SOS*",
        "*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*",
        ])
    _exit = "\n".join([
         "*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*",
         "*SOS*                               *SOS*",
         "*SOS*     SOS-TOOLKIT CLI EXIT      *SOS*",
         "*SOS*                               *SOS*",
         "*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*SOS*"
        ])

    enter = enter_msg or _enter
    exit = exit_msg or _exit

    InteractiveShellEmbed(banner1=enter, exit_msg=exit)(stack_depth=2)


#
###