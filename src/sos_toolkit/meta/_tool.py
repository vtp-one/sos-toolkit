from typing import Optional, Dict, List, Union, Callable, Annotated
from pydantic import BaseModel, Field
import rich
from pathlib import Path
from inspect import getfile

from sos_toolkit.meta._meta import MetaRepo, MetaRoot, MetaSchema, ModelGet, ModelDict
from sos_toolkit.meta._utils import valid_keys

class ToolObject(ModelGet):
    sos_schema: MetaSchema = Field(default=MetaSchema(), description="Tool Schema")
    key: str = Field(description="Tool Key")
    description: str = Field(default="None", description="Tool Description")
    meta: Dict = Field(default={}, description="Tool MetaData")
    function: Callable = Field(default=None, description="Tool Function")

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def with_context(self, __CTX__, *args, **kwargs):
        raise NotImplementedError()

        return self.function(__CTX__, *args, **kwargs)

    @classmethod
    def from_function(cls,
        function: Callable,
        key: Optional[str] = None,
        description: Optional[str] = None,
        sos_schema: Optional[List[Dict] | MetaSchema] = None,
        meta: Optional[Dict] = {}):

        key = key or function.__name__
        description = description or function.__doc__

        if description is None:
            e = f"NO DESCRIPTION PROVIDED: {key} - {function}"

        if isinstance(sos_schema, Dict):
            sos_schema = MetaSchema(**sos_schema)

        sos_schema = sos_schema or MetaSchema.from_function(function)

        obj = cls(
            key=key,
            description=description,
            sos_schema=sos_schema,
            meta=meta,
            function=function)

        return obj


class ToolRepo(MetaRepo):
    __OBJECT__ = ToolObject


class ToolRoot(MetaRoot):
    __REPO_OBJECT__ = ToolRepo


SOS_TOOL = ToolRoot()

#
# TODO
# - allow this to take values from the decorator
#
def sos_tool(function):
    file = getfile(function)
    namespace = Path(file).resolve().parent.name
    key = function.__name__

    try:
        SOS_TOOL.register(
            function=function,
            namespace=namespace,
            key=key,
            overwrite=False,
            validate=True)

    except Exception as exc:
        e = f"SOS_TOOL ERROR: {file} - {key} - {exc.__str__()}"
        rich.print(e)

    finally:
        return function