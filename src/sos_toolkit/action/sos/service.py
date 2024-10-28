from typing import Optional, Annotated, Callable
from pydantic import Field
import rich

from os import listdir
from os.path import isdir, join

from sos_toolkit.meta import SOSContext, sos_action, ResultRepo
from sos_toolkit.service import SERVICE_PATH

@sos_action
def service(
    target: Annotated[Optional[str], Field(description="The service to target")] = "",
    action: Annotated[Optional[str], Field(description="The target action to run")] = None,
):

    """Run SOS-Service Actions"""
    rich.print({"SOS_SERVICE":
            {
            "target":target,
            "action":action,
            }
        })

    runtime_config= {"service":{}}
    for service in listdir(SERVICE_PATH):
        if isdir(join(SERVICE_PATH, service)) and not service.startswith("_"):
            runtime_config["service"][service] = True

    if service != "local_data":
        runtime_config["service"].pop("local_data", None)

    __CTX__ = SOSContext.generate(
        system_file=False,
        local_file=False,
        user_file=False,
        root_file=False,
        runtime_config=runtime_config)

    if target != "":
        _target = f"service.{target}.action.{action}"

        if __CTX__.get(_target, None) is not None:
            result = __CTX__.run(_target)

        else:
            e = f"SERVICE TARGET DOES NOT SUPPORT ACTION: {_target}"
            rich.print(e)
            result = ResultRepo(result=e)

    else:
        result = ResultRepo()

        for service in __CTX__.service.keys():
            _target = f"service.{service}.action.{action}"

            if __CTX__.get(_target, None) is not None:
                _result = __CTX__.run(_target)

            else:
                e = f"SERVICE TARGET DOES NOT SUPPORT ACTION: {_target}"
                rich.print(e)
                _result = e

            result.set(service, _result)

    return result
