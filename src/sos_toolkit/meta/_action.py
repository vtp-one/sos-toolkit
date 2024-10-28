from typing import Optional, Dict, List, Union, Callable
from pydantic import BaseModel, Field, field_validator
from inspect import getfile
from pathlib import Path
import inspect
import rich

from sos_toolkit.meta._model import ModelParams
from sos_toolkit.meta._meta import MetaRepo, MetaRoot, MetaRunnable, MetaObject, MetaConfig

from sos_toolkit.meta._tool import ToolObject

###
# REGISTER AN ACTION
#
class ActionRepo(MetaRepo):
    __OBJECT__ = ToolObject

class ActionRoot(MetaRoot):
    __REPO_OBJECT__ = ActionRepo

SOS_ACTION = ActionRoot()

def sos_action(function):
    file = getfile(function)
    namespace = Path(file).resolve().parent.name
    key = function.__name__

    try:
        SOS_ACTION.register(
            function=function,
            namespace=namespace,
            key=key,
            overwrite=False,
            validate=True)

    except Exception as exc:
        e = f"SOS_ACTION ERROR: {file} - {key} - {exc.__str__()}"
        rich.print(e)

    finally:
        return function

#
###

###
# BUILD AN ACTION
#
class ActionParams(ModelParams):
    pass


class ActionTask(MetaRunnable):
    params: ActionParams = Field(default=ActionParams(), description="The parameters for the action")


class ActionObject(MetaObject):
    __METATASK__ = ActionTask


class ActionConfig(MetaConfig):
    __METAOBJECT__ = ActionObject

#
###
