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
# BUILD A HOOK
#
class HookParams(ModelParams):
    pass


class HookTask(MetaRunnable):
    params: HookParams = Field(default=HookParams(), description="The parameters for the hook")


class HookObject(MetaObject):
    __METATASK__ = HookTask


class HookConfig(MetaConfig):
    __METAOBJECT__ = HookObject


#
###