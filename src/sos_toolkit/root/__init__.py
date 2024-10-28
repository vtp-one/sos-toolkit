###
#
from pathlib import Path

ROOT_PATH = Path(__file__).parent.resolve()

#
###

#
# TODO
# - we want this information for use with version changes
# - this file should be four layers below the source directory
#   but that isn't always true depending on installation methods
# - need a better way to generate this or to figure out how to remove it entirely
#
TOOLKIT_PATH = Path(__file__).parent.parent.parent.parent.resolve()