###
# load tools
#
from importlib import import_module
from os import listdir
from os.path import isdir, isfile, basename, abspath, dirname, join

import rich

from sos_toolkit.meta._tool import ToolRepo, SOS_TOOL

tool_path = dirname(abspath(__file__))
__all__ = [ m for m in listdir(tool_path) if isdir(join(tool_path,m)) and not m.startswith("_")]

p = "sos_toolkit.tool"
for tool_root in __all__:
    file_list = [basename(f)[:-3] for f in listdir(join(tool_path, tool_root)) if basename(f).endswith(".py") and not basename(f).startswith("_")]

    for tool_file in file_list:
        try:
            import_path = f"{p}.{tool_root}.{tool_file}"
            module = import_module(import_path)

        except Exception as exc:
            rich.print(f"TOOL_FILE LOAD ERROR: {tool_root} - {tool_file} - {exc}")
            continue

#
###