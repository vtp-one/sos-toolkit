###
# load actions
#
from importlib import import_module
from os import listdir
from os.path import isdir, isfile, basename, abspath, dirname, join

import rich

from sos_toolkit.meta._action import ActionRepo, SOS_ACTION

action_path = dirname(abspath(__file__))
__all__ = [ m for m in listdir(action_path) if isdir(join(action_path, m)) and not m.startswith("_")]

p = "sos_toolkit.action"
for action_root in __all__:
    file_list = sorted([basename(f)[:-3] for f in listdir(join(action_path, action_root)) if basename(f).endswith(".py") and not basename(f).startswith("_")])

    for action_file in file_list:
        try:
            import_path = f"{p}.{action_root}.{action_file}"
            module = import_module(import_path)

        except Exception as exc:
            rich.print(f"ACTION LOAD ERROR: {action_root} - {action_file} - {exc}")
            continue

#
###