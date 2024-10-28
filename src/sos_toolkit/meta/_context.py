###
#
from typing import Literal, List, Dict, Annotated, Optional, Tuple, Any, Union
from collections.abc import MutableMapping, Sequence
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo
from collections import ChainMap
from os import environ, getcwd, chdir, listdir
from os.path import join as path_join
from os.path import exists as path_exists

import rich
from omegaconf import OmegaConf, DictConfig
from pathlib import Path
from copy import deepcopy

from sos_toolkit.meta import _utils as utils
from sos_toolkit.meta._model import ModelGet, ModelDict, ModelParams
from sos_toolkit.meta._meta import MetaConfig, MetaObject, MetaRunnable
from sos_toolkit.meta import _global
from sos_toolkit.meta._action import ActionConfig, ActionTask, ActionObject
from sos_toolkit.meta._service import ServiceConfig, ServiceTask, ServiceObject
from sos_toolkit.meta._hook import HookConfig, HookTask, HookObject

from sos_toolkit.meta._platform import get_platform

from sos_toolkit.meta._tool import SOS_TOOL
from sos_toolkit.meta._result import ResultData, ResultObject, ResultRepo
from sos_toolkit.meta._utils import valid_keys

from sos_toolkit.root import ROOT_PATH, TOOLKIT_PATH
from sos_toolkit.service import SERVICE_PATH
from sos_toolkit.__about__ import __version__

#
###

class MetaConfig(ModelGet):
    """System Meta-Configuration"""
    __PRESERVE__ = True
    __OVERWRITE__ = False

    sos_version: str = Field(default="0.0.0",
        description="The SOS Version the system was built for")
    sos_path: str = Field(default=str(TOOLKIT_PATH),
        description="The Current SOS-Toolkit path")
    system_name: str = Field(default="",
        description="The Name of the System")
    system_version: str = Field(default="",
        description="The Version of the System")
    system_internal: str = Field(default="",
        description="The Internal Directory for the System")
    system_description: str = Field(default="",
        description="The Description of the System")
    platform: str = Field(default_factory=get_platform,
        description="The Runtime Platform")
    profile: str = Field(default="default",
        description="The Runtime Profile")
    network: str = Field(default=_global.DEFAULT_NETWORK,
        description="The default network to use")
    sandbox: bool = Field(default=False,
        description="Run in SOS-Sandbox")

    system_path: str = Field(default_factory=getcwd,
        description="The System Path")
    is_installed: bool = Field(default=False,
        description="If the System has been Installed")
    input_method: Literal["CLI", "NONE"] = Field(default="CLI",
        description="The Input Method to Use")

    local_file: Optional[Union[bool, str]] = Field(default=False,
        description="The Local Config File Used")
    user_file: Optional[Union[bool, str]] = Field(default=False,
        description="The User Config File Used")
    system_file: Optional[Union[bool, str]] = Field(default=False,
        description="The System Config File Used")
    root_file: Optional[Union[bool, str]] = Field(default=False,
        description="The Root Config File Used")
    context_file: Optional[Union[bool, str]] = Field(default=_global.CONTEXT_FILE,
        description="The Context File Used")

    # should we include these?
    # or is the file path good enough?
    # makes log entries annyoing (too much context)
    # this could be used for introspection into where and object came from
    # but that will require fiddling with omegaconf
    # would also probably be slow
    #local_config: Dict = Field(default={}, description="Local config")
    #system_config: Dict = Field(default={}, description="System config")
    #root_config: Dict = Field(default={}, description="Root config")
    #runtime_config: Dict = Field(default={}, description="Runtime config")

class SystemNamespace(ModelDict):
    """Internal Namespace for a System"""
    __PRESERVE__ = True
    __OVERWRITE__ = False

class SOSContext(ModelGet):
    """Context State for a System"""
    __PRESERVE__ = True
    __OVERWRITE__ = False
    __TARGET__ = None
    __RESULT__ = None

    meta: MetaConfig = Field(description="The MetaConfig for the System")
    namespace: SystemNamespace = Field(default=SystemNamespace(),
        description="The SystemNamespace for the System")
    service: ServiceConfig = Field(default=ServiceConfig(),
        description="The ServiceConfig for the System")
    action: ActionConfig = Field(default=ActionConfig(),
        description="The ActionConfig for the System")
    hook: HookConfig = Field(default=HookConfig(),
        description="The HookConfig for the System")

    @classmethod
    def generate(cls,
        system_file: Annotated[Optional[Union[bool, str]],
            Field(description="The system config file")] = None,
        local_file: Annotated[Optional[Union[bool, str]],
            Field(description="The local config file")] = None,
        user_file: Annotated[Optional[Union[bool, str]],
            Field(description="The user config file")] = None,
        root_file: Annotated[Optional[Union[bool, str]],
            Field(description="The root config file")] = None,
        context_file: Annotated[Optional[Union[bool, str]],
            Field(description="The current context file")] = None,
        runtime_config: Annotated[Optional[Dict[str, str]],
            Field(description="Runtime config value dict")] = {},
        runtime_update: Annotated[Optional[List[Tuple[str, str]]],
            Field(description="Runtime config values using dot notation")] = [],
        meta_config: Annotated[Optional[Dict[str, str]],
            Field(description="Runtime meta dict")] = {},
        namespace_config: Annotated[Optional[Dict[str, str]],
            Field(description="Runtime namespace dict")] = {},
        resolve_services: Annotated[Optional[bool],
            Field(description="If resolve services during loading")] = True,
        resolve_variables: Annotated[Optional[bool],
            Field(description="If resolve variables during loading")] = True,
        persist: Annotated[Optional[bool],
            Field(description="If persist from previous context_file")] = False,
        ignore_version: Annotated[Optional[bool],
            Field(description="Ignore SOS-Toolkit Version Mismatch")] = True
    ):
        """Generate an SOSContext Object"""
        rich.print({"GENERATE CONTEXT":
                {
                "system_file":system_file,
                "local_file":local_file,
                "user_file":user_file,
                "root_file":root_file,
                "context_file":context_file,
                "runtime_config":runtime_config,
                "runtime_update":runtime_update,
                "meta_config":meta_config,
                "namespace_config":namespace_config,
                "resolve_variables":resolve_variables,
                "persist":persist,
                }
            })

        zc = lambda x: OmegaConf.create(x)

        #
        # TODO
        # - how to get local_file / root_file / system_file / context_file better
        # - need to check key names for invalid names
        if system_file is False:
            system_config = zc({})

        else:
            system_file = None if system_file == "" else system_file
            system_file = system_file or environ.get(_global.ENV_SYSTEM_FILE, _global.SYSTEM_FILE)
            system_file = Path(system_file).absolute()

            if not utils.valid_path(system_file):
                e = f"NO SYSTEM FILE AVAILABLE - [ {system_file} ] MISSING"
                raise RuntimeError(e)

            else:
                rich.print(f"LOAD SYSTEM_FILE: {system_file}")
                system_config = OmegaConf.load(system_file)

        cls._version(system_config, ignore_version)

        if local_file is False:
            local_config = zc({})

        else:
            local_file = None if local_file in [True, ""] else local_file
            local_file = local_file or environ.get(_global.ENV_LOCAL_FILE, _global.LOCAL_FILE)
            local_file = Path(local_file).absolute()

            if utils.valid_path(local_file):
                rich.print(f"LOCAL_FILE: {local_file}")
                local_config = OmegaConf.load(local_file)

            else:
                rich.print(f"LOCAL_FILE: None")
                local_file = False
                local_config = zc({})

        if user_file is False:
            user_config = zc({})

        else:
            user_file = None if user_file in [True, ""] else user_file
            user_file = user_file or environ.get(_global.ENV_USER_FILE, _global.USER_FILE)
            user_file = Path(user_file).absolute()

            if utils.valid_path(user_file):
                rich.print(f"USER_FILE: {user_file}")
                user_config = OmegaConf.load(user_file)

            else:
                rich.print(f"USER_FILE: None")
                user_file = False
                user_config = zc({})

        if root_file is False:
            root_config = zc({})

        else:
            root_file = None if root_file in [True, ""] else root_file
            root_file = root_file or path_join(ROOT_PATH, environ.get(_global.ENV_ROOT_FILE, _global.ROOT_FILE))
            root_file = Path(root_file).absolute()

            if utils.valid_path(root_file):
                rich.print(f"ROOT_FILE: {root_file}")
                root_config = OmegaConf.load(root_file)

            else:
                rich.print(f"ROOT_FILE: None")
                root_file = False
                root_config = zc({})

        if context_file is False:
            _context_file = False

        else:
            _context_file = None if context_file == "" else context_file
            context_file = _context_file or environ.get(_global.ENV_CONTEXT_FILE, _global.CONTEXT_FILE)
            context_file = Path(context_file).absolute()

        # check for persist
        #
        # TODO
        # - add services?
        # - anything else?
        # - should this be pushed to update instead?
        # - generate always constructs a complete context?
        # - trying to persist objects will cause problem => need to check for changes? good luck
        # - update needs action to work => this could handle the persist?
        #
        persist_list = ["namespace", "service"]
        if persist:
            if utils.valid_path(context_file):
                context_file = OmegaConf.load(context_file)
                persist_config = {}
                for key in persist_list:
                    persist_config[key] = context_file[key]

            else:
                e = f"PREVIOUS CONTEXT_FILE DOES NOT EXIST FOR PERSIST: {context_file}"
                raise RuntimeError(e)

        else:
            persist_config = {}

        # merge runtime options
        runtime_config = OmegaConf.merge(zc(runtime_config), zc({"meta":meta_config, "namespace":namespace_config}))

        # extract services
        system_service = system_config.pop("service", {})
        local_service = local_config.pop("service", {})
        user_service = user_config.pop("service", {})
        root_service = root_config.pop("service", {})
        runtime_service = runtime_config.pop("service", {})


        # merge configs
        config = OmegaConf.merge(root_config, user_config, system_config, local_config, runtime_config, persist_config)

        # force the platform
        config["meta"]["platform"] = config["meta"].get("platform", get_platform())

        # build the services
        if resolve_services:
            config["service"] = cls._service(
                platform=config["meta"]["platform"],
                system_service=system_service,
                local_service=local_service,
                user_service=user_service,
                root_service=root_service,
                runtime_service=runtime_service)

        else:
            config["service"] = system_service

        # update runtime settings
        for key, value in runtime_update:
            OmegaConf.update(config, key, value, force_add=True)

        # resolve the variables
        if resolve_variables:
            OmegaConf.resolve(config)

        # bundle the file paths
        if utils.valid_path(local_file):
            config["meta"]["local_file"] = local_file.as_posix()
        else:
            config["meta"]["local_file"] = None

        if utils.valid_path(user_file):
            config["meta"]["user_file"] = user_file.as_posix()
        else:
            config["meta"]["user_file"] = None

        if utils.valid_path(system_file):
            config["meta"]["system_file"] = system_file.as_posix()
        else:
            config["meta"]["system_file"] = None

        if utils.valid_path(root_file):
            config["meta"]["root_file"] = root_file.as_posix()
        else:
            config["meta"]["root_file"] = None

        if _context_file is False:
            config["meta"]["context_file"] = False

        elif _context_file is not None:
            config["meta"]["context_file"] = Path(_context_file).absolute().as_posix()

        elif (_context_file := config["meta"].get("context_file", None)):
            config["meta"]["context_file"] = Path(_context_file).absolute().as_posix()

        else:
            config["meta"]["context_file"] = context_file.as_posix()

        # bundle the base data
        # TODO
        # - need a better way to store the base data
        # - this is massive amount of redundant data
        #
        #config["meta"]["system_config"] = OmegaConf.to_container(system_config, resolve=False)
        #config["meta"]["local_config"] = OmegaConf.to_container(local_config, resolve=False)
        #config["meta"]["root_config"] = OmegaConf.to_container(root_config, resolve=False)
        #config["meta"]["runtime_config"] = OmegaConf.to_container(runtime_config, resolve=False)

        return cls.from_config(config)


    @classmethod
    def from_config(cls,
        config: Annotated[dict, Field(description="A dictionary for an SOSContext")]
    ):
        """Build an SOSContext object from a config dictionary"""

        # TODO_LABEL

        output_params = {}


        # meta
        meta = config.pop("meta")

        if isinstance(meta, DictConfig):
            meta = OmegaConf.to_container(meta, resolve=False)

        output_params["meta"] = MetaConfig(**valid_keys(meta))


        # namespace
        if (namespace := config.pop("namespace", None)) is None:
            namespace = {}

        else:
            if isinstance(namespace, DictConfig):
                namespace = OmegaConf.to_container(namespace, resolve=False)

        output_params["namespace"] = SystemNamespace(**valid_keys(namespace))


        # service
        service = ServiceConfig()
        if (_service := config.pop("service", None)) is not None:
            if isinstance(_service, DictConfig):
                _service = OmegaConf.to_container(_service, resolve=False)

            for key, value in _service.items():
                if hasattr(value, "keys") and "meta" in value.keys():
                    service.set(key, cls.from_config(value))

                else:
                    service.set(key, value)

        output_params["service"] = service


        # action
        action = config.pop("action", {})
        if isinstance(action, DictConfig):
            action = OmegaConf.to_container(action, resolve=False)

        output_params["action"] = ActionConfig.from_config(action, label="action")


        # hook
        hook = config.pop("hook", {})
        if isinstance(hook, DictConfig):
            hook = OmegaConf.to_container(hook, resolve=False)

        output_params["hook"] = HookConfig.from_config(hook, label="hook")


        # overwrite
        overwrite = config.get("overwrite", {})
        if isinstance(overwrite, DictConfig):
            overwrite = OmegaConf.to_container(overwrite, resolve=False)

        output_params["overwrite"] = overwrite


        # delete
        delete = config.get("delete", {})
        if isinstance(delete, DictConfig):
            delete = OmegaConf.to_container(delete, resolve=False)

        output_params["delete"] = delete

        return cls._overwrite(output_params)

    @classmethod
    def file_load(cls,
        context_file: Annotated[Optional[str], Field(description="The target context_file to load from")] = _global.CONTEXT_FILE,
        install_state: Annotated[Optional[bool], Field(description="The required is_installed state")] = None,
        run_hooks: Annotated[Optional[bool], Field(description="If run on_context_load hooks")] = True,
        ignore_version: Annotated[Optional[bool], Field(description="Ignore SOS-Toolkit Version Mismatch")] = True
    ):
        """Load an SOSContext object from a context_file"""
        context_file = None if context_file == "" else context_file
        context_file = context_file or MetaConfig.__fields__["context_file"].default
        context_file = Path(context_file).absolute()

        rich.print(f"LOADING CONTEXT - context_file: {context_file}")

        config = OmegaConf.load(context_file)

        #
        # TODO
        # - how to handle different sos-toolkit version
        # - git checkout from sos-toolkit root
        # - reload sos-toolkit module (good luck)
        # - reload obj
        # - continue
        #
        # for now just check version and ignore it
        #
        cls._version(config, ignore_version)

        # build the context
        obj = cls.from_config(config)

        #
        # TODO
        # currently paths are using absolute paths
        # but using relative paths might be better
        # but we need to be able to change working directory then
        # - how should this be handled?
        # - force change?
        # - toggle change?
        # - no change?
        #
        # for now error if not correct
        #
        if obj.meta.system_path is not None:
            if (cwd := getcwd()) != obj.meta.system_path:
                e = f"CURRENT WORKING DIRECTORY INCORRECT - current: {cwd} - context: {obj.meta.system_path}"
                raise RuntimeError(e)

            #chdir(obj.meta.system_path)

        if install_state is not None:
            if obj.meta.is_installed != install_state:
                e = f"SYSTEM INSTALL STATE INVALID: state: {obj.meta.is_installed} - required: {install_state}"
                raise RuntimeError(e)

        if run_hooks:
            obj.run("hook.on_context_load")

        return obj


    def file_save(self,
        context_file: Annotated[Optional[str], Field(description="The target context_file to save to")] = None,
        run_hooks: Annotated[Optional[bool], Field(description="If run on_context_save hooks")] = True
    ):
        """Save an SOSContext object to a context_file"""
        context_file = context_file or self.get("meta.context_file", _global.CONTEXT_FILE)

        rich.print(f"SAVING CONTEXT - context_file: {context_file}")

        if run_hooks:
            self.run("hook.on_context_save")

        self.__TARGET__ = None
        self.__RESULT__ = None
        OmegaConf.save(self.dict(), context_file)


    #
    # TODO
    # - allow providing params => (self, target, /, **args, **kwargs)
    # - need to figure out the best way to use positional args
    # - probably need to reimplement the entire order for run actions context <=> tool <=> object
    # - => MetaRunnable
    #
    def run(self,
        target: Annotated[str, Field(description="The target object to run")]
    ):
        """Run the target Runnable Object"""
        obj = self.get(target, None)
        if obj is None:
            e = f"RUN TARGET IS NONE: {target}"
            rich.print(e)
            return ResultRepo(result=e)

        elif isinstance(obj, (MetaConfig, MetaObject, MetaRunnable)):
            return obj(self)

        else:
            e = f"INVALID TARGET: {target} - obj: {type(obj)}"
            raise RuntimeError(e)


    def flatten(self,
        parent: Annotated[str, Field(description="The Parent Key for Compund Keys")] = "",
        sep: Annotated[str, Field(description="The seperator object for joining Compound Keys")] = "_"
    ):
        """Flatten an SOSContext object into a single layer dictionary of compound keys"""

        def _flatten(d, parent="", sep="_"):
            items = []

            if not hasattr(d, "items"):
                return [(parent, d)]

            for key, value in d.items():
                new_key = sep.join([parent, key]) if parent else key

                match value:
                    case MutableMapping() | ModelDict():
                        items.extend(_flatten(value, new_key, sep))

                    case ModelGet():
                        items.extend(_flatten(value.dict(), new_key, sep))

                    case str():
                        new_key = new_key.replace("-", "_")
                        items.append((new_key.upper(), value))

                    case Sequence():
                        for (n,v) in enumerate(value):
                            _new_key = sep.join([new_key, str(n)])
                            items.extend(_flatten(v, _new_key, sep))

                    case _:
                        continue

            return items

        f = {"meta":self.meta, "namespace":self.namespace, "service":self.service, "action":self.action}
        return dict(_flatten(f, parent, sep))


    @classmethod
    def _overwrite(cls, config):
        """Process the overwrite keys and return the SOSContext"""
        overwrite = config.pop("overwrite", {}) or {}
        delete = config.pop("delete", []) or []

        obj = cls(**config)
        if len(overwrite):
            for key, value in overwrite.items():
                obj.set(key, value, overwrite=True)

        if len(delete):
            rich.print(f"DELETE: {delete}")

            for key in delete:
                obj.remove(key)

        return obj


    @staticmethod
    def _version(config, ignore_version=False, exact_version=False):
        if (system := config.get("meta", {}).get("sos_version", None)):
            if exact_version:
                toolkit = __version__
                _system = system

            else:
                toolkit = __version__.split("v")[-1]
                _system = system.split("v")[-1]

            if _system != toolkit:
                e = f"SYSTEM_VERSION MISMATCH - system_version: {system} - sos-toolkit_version: {__version__}"
                if ignore_version:
                    rich.print(e)

                else:
                    raise RuntimeError(e)


    @staticmethod
    def _service(
        platform,
        system_service=None,
        local_service=None,
        user_service=None,
        root_service=None,
        runtime_service=None,
    ):
        """Build the Service Objects"""
        #
        # TODO
        # - how to load a service into sos-root / sos-local / sos-system
        # - useful but goes away from the purpose somewhat
        # - this should most likely be done by making services modular
        # - that will require dynamic installation of them somehow
        # - which brings us back to the sos_services implementation problems
        #
        system_service = system_service or {}
        runtime_service = runtime_service or {}

        service_set = OmegaConf.merge(system_service, runtime_service)

        output_service = {}
        while len(service_set):
            key = list(service_set.keys())[0]
            _system = service_set.pop(key)
            rich.print(f"CONTEXT.SERVICE - start: {key}")

            match _system:
                case MutableMapping():
                    pass

                case bool():
                    if _system is False:
                        continue

                    _system = {}

                case _:
                    e = f"INVALID _SYSTEM: {key} - {type(_system)}"
                    raise RuntimeError(e)

            #
            # CHECK SERVICE ALREAD LOADED
            #
            if key in output_service.keys():
                #
                # TODO
                # - handle version / namespace collisions
                #
                # for now just ignore them since we don't have service versions
                #
                continue

            #
            # CHECK SERVICE EXISTS
            #
            service_root = path_join(SERVICE_PATH, key)
            if not path_exists(service_root):
                e = f"SERVICE NOT INSTALLED: {key}"
                raise RuntimeError(e)

            #
            # CHECK PLATFORM
            #
            service_platform = path_join(service_root, "platform", platform)
            if not path_exists(service_platform):
                default_path = path_join(service_root, "platform", "default")
                if not path_exists(default_path):
                    e = f"SERVICE DOES NOT SUPPORT PLATFORM AND NO DEFAULT: {platform} - {key}"
                    raise RuntimeError(e)

                else:
                    rich.print(f"SERVICE DOES NOT SUPPORT PLATFORM - WILL ATTEMPT TO USE DEFAULT: {key}")
                    service_platform = default_path
                    #platform = "default"

            # CHECK SERVICE FILE
            service_file = path_join(service_platform, "sos-service.yaml")
            if not path_exists(service_file):
                e = f"SERVICE FILE DOES NOT EXIST: {key}"
                raise RuntimeError(e)

            _output = SOSContext.generate(
                system_file=service_file,
                local_file=False,
                user_file=False,
                root_file=False,
                meta_config={"platform":platform, "system_path":service_root, "context_file":False},
                resolve_services=False,
                resolve_variables=False)

            # MERGE CONFIGS
            _root = root_service.get(key, {})
            _user = user_service.get(key, {})
            _local = local_service.get(key, {})
            _runtime = runtime_service.get(key, {})
            _output = OmegaConf.merge(_output.dict(), _root, _user, _system, _local)

            # HANDLE SUB-SERVICES
            _sub = False
            for _key, _value in _output.service.items():
                if _key not in output_service:
                    _sub = True

                if _key not in service_set and _key != key:
                    rich.print(f"CONTEXT.SERVICE - add: {_key}")
                    service_set[_key] = _value

            _output.service = {}

            # OUTPUT
            if _sub:
                # service has dependencies
                # - need to run them first
                # - readd this service to the processing list
                # - THIS COULD INFINITE LOOP IF SERVICE DEPDENDENCY FAILS
                # - would be nice to run this check earlier so we don't need to compute the complete service
                # - but that could retrun a false negative
                rich.print(f"CONTEXT.SERVICE - recycle: {key}")
                service_set[key] = _system

            else:
                #
                # service computed
                # - add to output
                #
                rich.print(f"CONTEXT.SERVICE - output: {key}")
                output_service[key] = _output

        return output_service
