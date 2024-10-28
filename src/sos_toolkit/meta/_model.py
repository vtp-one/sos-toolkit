from typing import Literal, Callable, ClassVar, Type, List, Optional, Union, Any, Dict, Annotated, _AnnotatedAlias, _GenericAlias, _SpecialForm, _CallableType
from pydantic import BaseModel, Field, create_model, validate_call, field_validator
from inspect import signature as inspect_signature
from collections.abc import MutableMapping, Sequence

import rich
import omegaconf

from sos_toolkit.meta._utils import valid_keys, is_idx, parse_idx


class ModelGet(BaseModel):
    __PRESERVE__ = False
    __OVERWRITE__ = True
    __LABEL__ = None

    def _get(self, name, **kwargs):
        try:
            # do we need this still?
            valid_keys(name)

            # check if default is provided or not
            if "default" in kwargs:
                result = getattr(self, name, kwargs.get("default"))

            else:
                result = getattr(self, name)

            # not allowed to get self functions
            # => should extend this to work with __PRESERVE__ => __HIDDEN__
            if callable(result) and getattr(result, "__self__", None) == self:
                e = f"SHADOWED CALLABLE - {name}"
                raise ValueError(e)

            return result

        except Exception as exc:
            # try to fall back to use a dict() method before we raise
            r = None
            try:
                r = self.dict().get(name)

            except:
                pass

            if r is None:
                raise

            else:
                return r


    def get(self, *args, **kwargs):
        _default = False
        if len(args) > 2:
            # too many args
            raise RuntimeError()

        if len(args) == 1:
            # one arg => should be name
            name = args[0]
            get_default = True

        elif len(args) == 2:
            # two arg => (name, default)
            name = args[0]
            default = args[1]
            _default = True
            get_default = False

        elif len(args) == 0:
            # no args
            if (name := kwargs.get("name")) is None:
                e = f"NO NAME PROVIDED"
                raise RuntimeError(e)

            get_default = True

        if get_default:
            # check kwargs for default
            if (default := kwargs.get("default")):
                _default = True

        match name:
            case str():
                pass

            case Sequence():
                # name is a list => should be [name, default]
                if len(name) > 1:
                    if _default:
                        e = f"CAN NOT USE COUPLED NAME/DEFAULT WHEN DEFAULT PROVIDED: {name} - {default}"
                        raise RuntimeError(e)

                    name, default = name
                    _default = True

                else:
                    name = name[0]

            case MutableMapping():
                # name is a dict {name, default}
                if "default" in name.keys():
                    if _default:
                        # default was provided as a kwarg and in the name dict
                        e = f"CAN NOT USE COUPLED NAME/DEFAULT WHEN DEFAULT PROVIDED: {name} - {default}"
                        raise RuntimeError(e)

                    default = name.pop("default")
                    _default = True

                name = name.pop("name")

            case _:
                e = f"INVALID TYPE FOR NAME: {type(name)}"
                raise RuntimeError(e)

        try:
            # will error if name is not a string
            _name = name.split(".")

            if len(_name) == 0:
                # no name => shouldnt get here
                raise RuntimeError()

            elif len(_name) == 1:
                # current level object
                # check if the name includes a list index => [N]
                if is_idx(_name[0]):
                    # parse the name to get a list_idx [N]
                    _obj, _idx = parse_idx(_name[0])
                    return self._get(name=_obj).__getitem__(_idx)

                elif _default:
                    return self._get(name=_name[0], default=default)

                else:
                    return self._get(name=_name[0])

            else:
                # lower level object
                # get the current level object
                # and generate the remainder
                obj = self.get(_name[0])
                rem = ".".join(_name[1:])

                if isinstance(obj, omegaconf.DictConfig | dict):
                    # make sure the obj is a ModelDict
                    obj = ModelDict(**obj)
                    self.set(_name[0], obj, True)

                if not callable(obj_get := getattr(obj, "get", None)):
                    # shouldnt get here
                    # but we want to know the type that brought us here
                    e = f"INVALID OBJ FOR GET: {type(obj)} - {type(obj_get)}"
                    raise RuntimeError(e)

                if _default:
                    return obj_get(name=rem, default=default)

                else:
                    return obj_get(name=rem)

        except Exception as exc:
            # TODO
            # - this currently destroys all errors if a default was provided
            # - need to change this to only catch the errors we want (what are those?)
            # - or at least log them
            #
            if _default:
                return default

            else:
                raise


    def _set(self, name, value, overwrite=False, force=False):
        valid_keys(name)

        # get the obj we are trying to set
        obj = getattr(self, name, None)

        # not allowed to set self functions
        if callable(obj) and getattr(obj, "__self__", None) == self:
            e = f"CAN NOT OVERWRITE OBJ METHOD: {name}"
            raise RuntimeError(e)

        # if obj already exists and not overwrite
        elif obj and not overwrite:
            e = f"NAME ALREADY EXISTS: {name}"
            raise ValueError(e)

        # if object is protected
        elif obj and getattr(obj, "__OVERWRITE__", True) is False and force is False:
            e = f"CAN NOT OVERWRITE OBJECT: {name}"
            raise RuntimeError(e)

        return setattr(self, name, value)


    def set(self, name, value, overwrite=False):
        _name = name.split(".")

        if len(_name) == 0:
            # no name provided
            raise RuntimeError()

        elif len(_name) == 1:
            # local name
            # check for list_idx
            if is_idx(_name[0]):
                # handle list object set
                _obj, _idx = parse_idx(_name[0])
                _obj = self.get(_obj, [])
                _obj.__setitem__(_idx, value)
                self._set(_name[0], value, overwrite)

            return self._set(_name[0], value, overwrite)

        else:
            # embeded object
            # check for list_idx
            if is_idx(_name[0]):
                _obj, _idx = parse_idx(_name[0])

                # check that the target obj name exists
                if not self.has(_obj):
                    # creating a new list in the obj
                    _list = []
                    self.set(_obj, _list, True)

                else:
                    # TODO
                    # need to copy the preexisting list to make sure it updates
                    # - how to avoid this copy
                    _list = [*self.get(_obj)]
                    self.set(_obj, _list, True)

                # make sure the list is long enough for what we are setting
                # TODO => BUG
                # - this won't handle list object types and instead just populates with a ModelDict
                # - that could cause problems with using the objects latter on
                # - should this just error?
                while (len(_list) - 1) < _idx:
                    _list.append(ModelDict())

                # get the object we want from the list
                obj = _list[_idx]
                if not isinstance(obj, ModelGet):
                    # TODO => BUG
                    # - this can't handle nested lists
                    # - possible but then we need to handle multiple idx as well [N1][N2]
                    # if the object isn't a ModelDict => make it one
                    obj = ModelDict(**obj)
                    _list[_idx] = obj

            elif not self.has(_name[0]):
                # the object doesn't exist
                # create a new one and set
                obj = ModelDict()
                self.set(_name[0], obj, True)

            else:
                # get the object
                obj = self.get(_name[0], None)
                if obj is None:
                    # shouldnt get here
                    # object doesn't exist
                    obj = ModelDict()
                    self.set(_name[0], obj, True)

                elif not isinstance(obj, ModelGet):
                    # TODO
                    # force the object to be a ModelDict
                    # - this will error on non-dict obj
                    obj = ModelDict(**obj)
                    self.set(_name[0], obj, True)

            # generate the remainder name and call set on the obj with it
            rem = ".".join(_name[1:])

            return obj.set(rem, value, overwrite)


    def _remove(self, name):
        if (obj := self.get(name, None)) is not None:
            if getattr(obj, "__PRESERVE__", False) is True:
                e = f"CAN NOT REMOVE PRESERVED OBJECT: {name}"
                raise RuntimeError(e)

            delattr(self, name)


    def remove(self, name):
        _name = name.split(".")

        if len(_name) == 0:
            raise RuntimeError()

        elif len(_name) == 1:
            return self._remove(_name[0])

        else:
            obj = self.get(_name[0])

            if not isinstance(obj, ModelGet):
                e = f"INVALID REMOVE KEY - GET TYPE INVALID: {name} - {type(obj)}"
                raise RuntimeError(e)

            rem = ".".join(_name[1:])

            return obj.remove(rem)


    def has(self, name):
        #
        # TODO
        # - make this lookup faster?
        # - we don't need the entire get chain
        # - we could just use the dot notation, but that won't handle lists
        #
        try:
            self.get(name)
            return True

        except:
            return False


    def print(self):
        rich.print(self)


    def pp(self):
        return rich.pretty.pretty_repr(self)


    def __getitem__(self, name):
        # list_idx support
        return self.get(name)


    def __setitem__(self, name, value):
        # list_idx support
        return self.set(name, value, overwrite=True)


class ModelDict(ModelGet):
    class Config():
        extra = "allow"
        arbitrary_types_allowed = True

    def values(self):
        return self.model_extra.values()

    def items(self):
        return self.model_extra.items()

    def keys(self):
        return self.model_extra.keys()

    def __dir__(self):
        return self.keys()


class ModelParams(ModelDict):
    @classmethod
    def from_schema(cls, schema):
        raise RuntimeError()
        return create_model("ModelParams", __base__=cls, **schema_kwargs)
