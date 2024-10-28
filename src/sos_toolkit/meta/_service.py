from typing import Optional, Dict, List, Union, Callable
from pydantic import BaseModel, Field

from sos_toolkit.meta._model import ModelParams
from sos_toolkit.meta._meta import MetaRepo, MetaRoot, MetaRunnable, MetaObject, MetaConfig

###
#
class ServiceParams(ModelParams):
    pass


class ServiceTask(MetaRunnable):
    params: ServiceParams = Field(default=ServiceParams(), description="The parameters for the service")


class ServiceObject(MetaObject):
    __METATASK__ = ServiceTask


class ServiceConfig(MetaConfig):
    __METAOBJECT__ = ServiceObject

#
###
