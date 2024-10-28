from typing import (
    Literal,
    Callable,
    ClassVar,
    Type,
    List,
    Optional,
    Union,
    Any,
    Dict,
    Annotated,
    _AnnotatedAlias,
    _GenericAlias,
    _SpecialForm,
    _CallableType
    )

from pydantic import BaseModel, Field, create_model, validate_call, field_validator
from inspect import signature as inspect_signature
from collections.abc import MutableMapping, Sequence
from types import MethodType

import rich
from copy import deepcopy
from pathlib import PosixPath
from os.path import join as path_join

from sos_toolkit.meta import _global
from sos_toolkit.meta._exception import RuntimeBreak
from sos_toolkit.meta._model import ModelGet, ModelDict, ModelParams
from sos_toolkit.meta._utils import valid_keys, is_idx, parse_idx, ipython_portal
from sos_toolkit.meta._result import ResultRepo, ResultObject

class MetaRepo(ModelDict):
    __OBJECT__: ClassVar[ModelGet] = ModelGet

    @classmethod
    def register(cls, namespace: Annotated[str, Field(description="Namespace for Repo")]
    ):
        """Create a new Repo with a namespace"""
        valid_keys(namespace)

        return create_model(f"{cls.__name__}_{namespace}", __base__=cls)()


class MetaRoot(ModelDict):
    __REPO_OBJECT__: ClassVar[MetaRepo] = MetaRepo

    def register(self,
        function: Annotated[Callable, Field(description="Target function")],
        namespace: Annotated[str, Field(description="Target Namespace")],
        key: Annotated[str, Field(description="Target key")],
        meta: Annotated[Optional[Dict], Field(description="Target MetaData")] = {},
        description: Annotated[Optional[str], Field(description="Target Description")] = None,
        overwrite: Annotated[Optional[bool], Field(description="If overwrite preexisting target")] = False,
        validate: Annotated[Optional[bool], Field(description="If function should be validated")] = True,
    ):
        """Register a Function to a Root Object"""

        valid_keys(namespace)

        if not callable(function):
            e = f"FUNCTION INVALID - NOT CALLABLE: {function}"
            raise RuntimeError(e)

        repo = self.get(namespace, None)

        if repo is None:
            repo = self.__REPO_OBJECT__.register(namespace=namespace)

        if not isinstance(repo, self.__REPO_OBJECT__) and not issubclass(repo.__base__, self.__REPO_OBJECT__):
            e = f"NAMESPACE INVALID - SHADOWS OBJECT: {namespace}"
            raise RuntimeError(e)

        if (tool := repo.get(key, None)) is not None:
            #
            # TODO: CIRCULAR_IMPORT
            # - ToolObject <=> _meta
            #
            from sos_toolkit.meta._tool import ToolObject

            if not isinstance(tool, ToolObject):
                e = f"TOOL KEY INVALID - KEY SHADOWS OBJECT: {namespace} - {key}"
                raise RuntimeError(e)

            if not overwrite:
                e = f"TOOL EXISTS - OVERWRITE FALSE: {namespace} - {key}"
                raise RuntimeError(e)

        if validate:
            #
            # TODO
            # - validate is currently disabled due to excessive logging
            # - how can we extract this step from the stack while still
            #   allowing validation errors to work correctly
            #
            #function = validate_call(function)
            pass

        valid_keys(key)
        tool = self.__REPO_OBJECT__.__OBJECT__.from_function(
                function=function,
                key=key,
                description=description,
                meta=meta
            )

        repo.set(key, tool)

        if not hasattr(self, namespace):
            self.set(namespace, repo)



class MetaAnnotation(ModelGet):
    key: str = Field(description="Object Name")
    description: str = Field(description="Object Description")
    kind: Union[Type, _GenericAlias, _SpecialForm, _CallableType] = Field(description="Object Type")
    default: Optional[Any] = Field(default=None, description="Object Default")
    meta: Optional[Dict] = Field(default={}, description="Object MetaData")

    class Config():
        arbitrary_types_allowed = True


class MetaSchema(ModelDict):
    @classmethod
    def generate(cls, **kwargs):
        raise RuntimeError()
        _kwargs = {}
        for k,v in kwargs:
            if isinstance(v, dict):
                v = MetaAnnotation(**v)

            if not isinstance(k, str) or not isinstance(v, MetaAnnotation):
                e = f"INVALID MetaSchema OBJECT: {k}"
                raise ValueError(e)

            _kwargs[k] = (MetaAnnotation, v)

        return create_model("MetaSchema", __base__=cls, **_kwargs)

    def validate(self, **kwargs):
        _kwargs = {}

        for k, v in self.fields:
            _v = kwargs.get(k, None)

            if v.default is None and _v is None:
                e = f"VALIDATE FAIL - MISSING VALUE: {k}"
                raise ValueError(e)

            _kwargs[k] = v.validate(_v)

        return _kwargs

    @classmethod
    def from_function(cls, func):
        if not callable(func):
            e = f"FUNC NOT CALLABLE - {func}"
            raise TypeError(e)

        signature = inspect_signature(func)
        parameters = signature.parameters

        _schema = {}
        for key, value in parameters.items():
            if not isinstance(value.annotation, _AnnotatedAlias):
                e = f"INVALID ANNOTATION - key: {key} - value: {value}"
                raise ValueError(e)

            annotation = {}
            annotation["key"] = key
            annotation["description"] = value.annotation.__metadata__[0].description
            annotation["kind"] = value.annotation.__args__[0]
            annotation["default"] = value.default
            annotation["meta"] = {}

            _schema[key] = MetaAnnotation(**annotation)

        return cls(**_schema)



class MetaCondition(ModelGet):
    label: Optional[str] = Field(default=None, description="Label for the Condition Object")
    ctx_key: str = Field(description="Target")
    #
    # TODO
    # - constrain list to bool / str
    # - allow conditions to be different comparison
    #
    valid: Optional[Union[bool, str, List]] = Field(default=None, description="Valid Values for Condition to be True")
    comparison: Optional[Literal["in", "equal", "range", "=", "<", ">", ">=", "<="]] = Field(default="in", description="Comparison Type for Condition")
    raise_exc: bool = Field(default=True, description="If raise on condition false")
    is_inverse: bool = Field(default=False, description="If return inverse result")
    context_value: Optional[Any] = Field(default=None, description="Value Used for Resolve")
    result: Optional[bool] = Field(default=None, description="Result of Resolve")

    def resolve(self, context, raise_exc: Optional[bool] = None):
        if raise_exc is None:
            raise_exc = self.raise_exc

        match self.comparison:
            case "in" | "equal":
                if isinstance(self.valid, list):
                    list_none = None in self.valid

                else:
                    list_none = False

                if self.valid is None or list_none:
                    if (_value := context.get(self.ctx_key, None)) is not None and context.has(self.ctx_key):
                        if isinstance(self.valid, list) and _value is not None:
                            self.context_value = _value
                            if _value in self.valid:
                                self.result = True

                            else:
                                self.result = False
                                #EXC

                        else:
                            self.context_value = _value
                            self.result = False
                            #EXC

                    else:
                        self.context_value = _value
                        self.result = True

                else:
                    _value = context.get(self.ctx_key, None)
                    self.context_value = _value
                    if isinstance(self.valid, list):
                        if _value not in self.valid:
                            self.result = False
                            #EXC

                        else:
                            self.result = True

                    else:
                        if _value != self.valid:
                            self.result = False
                            #EXC

                        else:
                            self.result = True

                e1 = self.is_inverse and self.result == True
                e2 = not self.is_inverse and self.result == False
                if raise_exc and (e1 or e2):
                    e = f"CONDITION FAILED: {self} - {e1} - {e2}"
                    raise ValueError(e)

                elif e1:
                    return False

                elif self.is_inverse:
                    return True

                else:
                    return self.result

            case _:
                e = f"COMPARISON NOT IMPLEMENTED FOR CONDITION: {self.comparison}"
                raise RuntimeError(e)


# TODO
# - fix typing for data
class MetaResolvable(ModelGet):
    label: Optional[str] = Field(default=None, description="Label for the object")
    result: Optional[str] = Field(default=None, description="Target for the resolved object")
    data: Union[
        str,
        Dict[str, Optional[Any]],
        List[Dict[str, Optional[Any]]]] = Field(description="List of sources to resolve")
    default: Optional[str] = Field(default=None, description="Default Value for Resolve")
    format_string: Optional[str] = Field(default=None, description="Format String for Combining Objects")
    path_join: Optional[bool] = Field(default=False, description="If Path Join Objects")
    to_list: Optional[bool] = Field(default=False, description="If return list of values")
    allow_none: Optional[bool] = Field(default=False, description="If return None or Default")

    def __call__(self, source, result = None):
        # handle source
        match self.data:
            case str():
                if self.default:
                    if (value := source.get(self.data, self.default)) is None and not self.allow_none:
                        value = self.default

                else:
                    value = source.get(self.data)

            case Sequence():
                objects = {}
                for (n, obj) in enumerate(self.data):
                    # TODO
                    # - test this
                    # allow recursive resolvables
                    if "label" in obj.keys():
                        _target = obj.pop("result", str(n))
                        value = MetaResolvable(**obj)(source)

                    elif (_source := obj.get("source", None)) is None:
                        _target = obj.get("target", str(n))
                        value = obj.get("default")

                    elif (_default := obj.get("default", None)) is not None:
                        _target = obj.get("target", str(n))
                        if (value := source.get(_source, default=_default)) is None and not self.allow_none:
                            value = _default

                    else:
                        _target = obj.get("target", str(n))
                        value = source.get(_source)

                    objects[_target] = value

                if self.path_join:
                    value = path_join(*objects.values())

                elif self.format_string is not None:
                    value = self.format_string.format(**objects)

                elif self.to_list:
                    value = list(objects.values())

                else:
                    value = objects

            case MutableMapping():
                if (_source := self.data.get("source", None)) is None:
                    if (_default := self.data.get("default", None)) is None:
                        e = f"NO SOURCE OR DEFAULT PROVIDED - LABEL: {self.label}"
                        raise RuntimeError(e)

                    value = _default

                elif (_default := self.data.get("default", None)) is not None:
                     if (value := source.get(_source, default=_default)) is None and not self.allow_none:
                        value = _default

                else:
                    value = source.get(_source)

            case _:
                e = f"INVALID SOURCE TYPE: {type(source)} - LABEL: {self.label}"
                raise RuntimeError(e)

        # result
        if self.result is not None and result is not None:
            result.set(self.result, value, overwrite=True)

        return value



#
# TODO
# - allow a condition to be a runnable object => result True / False
# - make all condition runnable objects?
# - make condition a resolveable object?
#
class MetaRunnable(ModelGet):
    label: Optional[str] = Field(default=None, description="The Runnable Label")
    tool: str = Field(description="The tool to use")
    disabled: bool = Field(default=False, description="If is disabled")
    condition: Optional[Union[MutableMapping, MetaCondition, List[MetaCondition]]] = Field(default=[], description="Condition Object")
    params: ModelParams = Field(default=ModelParams(), description="The parameters")
    context_map: Optional[List[MetaResolvable]] = Field(default=[], description="List of MetaResolvable Objects to map from Context to Params")
    result_map: Optional[List[MetaResolvable]] = Field(default=[], description="List of MetaResolvable Objects ot map from Result to Context")
    callbacks: Optional[List[Union["MetaRunnable", "MetaObject", "MetaConfig"]]] = Field(default=[], description="List of Callbacks")

    @field_validator("condition")
    @classmethod
    def validate_condition(cls, value):
        if isinstance(value, MutableMapping):
            return [MetaCondition(**value)]

        elif isinstance(value, list):
            z = []
            for v in value:
                match v:
                    case MutableMapping():
                        v = MetaCondition(**v)

                    case MetaCondition():
                        pass

                    case _:
                        raise ValueError("CONDITION INVALID")

                z.append(v)

            return z

        else:
            raise ValueError("CONDITION INVALID")


    def check_enabled(self, __CTX__):
        if self.disabled:
            return False

        for cond in self.condition:
            if not isinstance(cond, MetaCondition):
                cond = MetaCondition(**cond)

            if cond.resolve(context=__CTX__, raise_exc=False) is False:
                return False

        return True


    def __call__(self, __CTX__):
        #
        # TODO
        # - this should tell why it it isn't enabled
        # - direct disable vs condition
        # - not easy to do since that gets run in check_enabled not here
        #
        rich.print(f"METARUNNABLE.__CALL__ :::: {self.label}")
        result = None
        try:
            if not self.check_enabled(__CTX__=__CTX__):
                rich.print(f"NOT RUNNING OBJECT - NOT ENABLED: {self.label}")
                return ResultObject(condition=self.condition)

            # initial run
            result = self._run(__CTX__)
            callbacks = deepcopy(self.callbacks)
            callbacks.reverse()
            result = self._result(__CTX__, result)

            # callbacks
            while len(callbacks):
                cb = callbacks.pop()
                if not isinstance(cb, MetaRunnable):
                    #
                    # TODO
                    # - metaobj labels
                    #
                    rich.print(f"CALLBACK METAOBJ - {type(cb)}")
                    cb.__LABEL__ = f"CB::{self.__LABEL__}"
                    result = cb(__CTX__)

                else:
                    if not cb.check_enabled(__CTX__=self):
                        rich.print(f"NOT RUNNING CALLBACK - NOT ENABLED: {cb}")
                        continue

                    else:
                        rich.print(f"CALLBACK._RUN :::: {cb.label}")

                    result = cb._run(__CTX__)
                    result = cb._result(__CTX__, result)

                # add callback => callbacks
                _cb = cb.get("callbacks", [])
                _cb.reverse()
                callbacks.extend(_cb)

                # add result callbacks => callbacks
                _cb = result.get("callbacks", [])
                _cb.reverse()
                callbacks.extend(_cb)

            __CTX__.set("__RESULT__", None, True)

            return result

        except RuntimeBreak as exc:
            return exc

        except Exception as exc:
            #
            # if debug => breakpoint else raise / handle_exc
            #
            rich.print({"RUN_ERROR":
                {
                "label":self.label,
                "exc_type":type(exc),
                "exc":exc}
                })

            if _global.DEBUG_ENABLE:
                ipython_portal()

            raise


    def _run(self, __CTX__):
        """Run this Object"""

        ####
        # TODO - CIRCULAR_IMPORT
        # - fix circular import for SOS_TOOL
        #
        from sos_toolkit.meta._tool import SOS_TOOL
        #
        ###

        tool = deepcopy(self.tool)
        params = deepcopy(self.params)
        context_map = deepcopy(self.context_map)
        _tool = SOS_TOOL.get(self.tool)

        for obj in context_map:
            obj(__CTX__, params)

        if "__RESULT__" in _tool.sos_schema.keys():
            if __CTX__.__RESULT__ is None:
                e = f"TOOL EXPECTS A RESULTOBJECT BUT NONE PROVIDED: {tool}"
                raise RuntimeError(e)

            params.set("__RESULT__", __CTX__.__RESULT__, True)

        # call tool
        if "__CTX__" in _tool.sos_schema.keys():
            try:
                setattr(__CTX__, "__tool__", MethodType(_tool, __CTX__))
                result = __CTX__.__tool__(**params.dict())

            finally:
                setattr(__CTX__, "__tool__", None)

        else:
            result = _tool(**params.dict())

        return result


    def _result(self, __CTX__, result):
        """Parse a result object"""
        tool = deepcopy(self.tool)
        params = deepcopy(self.params)
        result_map = deepcopy(self.result_map)

        if result is None:
            result = ResultObject(called_tool=tool, called_params=params, data=None)

        elif isinstance(result, ResultObject):
            result.called_tool = tool
            result.called_params = params

        elif isinstance(result, dict):
                _params = {}
                for k in ResultObject.__fields__:
                    if value := result.pop(k, None):
                        _params[k] = value

                _params["called_tool"] = tool
                _params["called_params"] = params
                result = ResultObject(**_params, data=result)

        else:
            result = ResultObject(called_tool=tool, called_params=params, data={"result":result})

        __CTX__.set("__RESULT__", result, True)

        for obj in result_map:
            obj(result.data, __CTX__)

        return result


class MetaObject(ModelDict):
    __METATASK__ = None


    @classmethod
    def from_config(cls, config: Optional[dict], label: Optional[str] = None):
        match config:
            case None:
                result = None

            case MutableMapping():
                if "tool" in config:
                    # TODO::__TARGET__
                    # TODO::__LABEL__
                    result = cls.__METATASK__(**config)
                    result.__LABEL__ = label

                else:
                    result = cls()
                    result.__LABEL__ = label
                    for key, obj in config.items():
                        # TODO::__TARGET__
                        # TODO::__LABEL__
                        if key == "__TARGET__":
                            result.set(key, obj)

                        else:
                            result.set(key, cls.from_config(obj, label=key))

            case str() | bool() | int() | float():
                result = config

            case PosixPath():
                result = str(config)

            case _:
                e = f"OBJ NOT SUPPORTED: {type(config)}"
                raise RuntimeError(e)

        return result


    def __call__(self, __CTX__):
        result = ResultRepo()

        if self.get("disabled", False):
            rich.print(f"NOT RUNNING OBJECT - NOT ENABLED: {self.__LABEL__}")

        else:
            # TODO::__TARGET__
            if (target := self.get("__TARGET__", None)):
                raise NotImplementedError()
                __CTX__.set("__TARGET__", target)

            for key, obj in self.items():
                if key == "disabled":
                    continue

                rich.print(f"METAOBJECT.__CALL__.{self.__LABEL__}.{key}")

                if isinstance(obj, (MetaRunnable, MetaObject, MetaConfig)):
                    _result = obj(__CTX__)
                    result.set(key, _result)

                    if isinstance(_result, RuntimeBreak):
                        break

                elif isinstance(obj, MutableMapping):
                    obj = MetaRunnable(**obj)
                    _result = obj(__CTX__)
                    result.set(key, _result)

                    if isinstance(_result, RuntimeBreak):
                        break

                else:
                    e = f"INVALID OBJ TYPE: {type(obj)} - {key} - {self.__LABEL__}"
                    raise RuntimeError(e)

        return result


class MetaConfig(ModelDict):
    __PRESERVE__ = True
    __METAOBJECT__ = None


    @classmethod
    def from_config(cls, config: dict, label: Optional[str] = None):
        result = cls()
        # TODO_LABEL
        result.__LABEL__ = label

        match config:
            case None:
                pass

            case MutableMapping():
                for key, obj in config.items():
                    # TODO::__TARGET__
                    # TODO::__LABEL__
                    if key == "__TARGET__":
                        result.set(key, obj)

                    else:
                        result.set(key, cls.__METAOBJECT__.from_config(obj, label=key))

            case _:
                e = f"OBJ NOT SUPPORTED: {type(config)}"
                raise RuntimeError(e)

        return result

    def __call__(self, __CTX__):
        result = ResultRepo()

        if self.get("disabled", False):
            rich.print(f"NOT RUNNING OBJECT - NOT ENABLED: {self.__LABEL__}")

        else:
            # TODO::__CONDITION__
            # TODO::__TARGET__
            if (target := self.get("__TARGET__", None)):
                __CTX__.set("__TARGET__", target)

            for key, obj in self.items():
                if isinstance(obj, (MetaRunnable, MetaObject, MetaConfig)):
                    rich.print(f"METACONFIG.__CALL__.{self.__LABEL__}.{key}")
                    _result = obj(__CTX__)
                    result.set(key, _result)

                    if isinstance(_result, RuntimeBreak):
                        break

                else:
                    e = f"INVALID OBJ TYPE: {type(obj)} - {key} - {self.__LABEL__}"
                    raise RuntimeError(e)


        return result


MetaRunnable.update_forward_refs()
