###
#
from os import environ
DEBUG_ENABLE = environ.get("SOS_DEBUG", False)
ALLOW_DELETE = environ.get("SOS_DELETE", True)

#
###

###
#
SOS_SOURCE = "https://github.com/vtp-one/sos-toolkit"
DEFAULT_NETWORK = "sos"

#
###

###
#
ACTION_ROOT = "sos_toolkit.action"
TOOL_ROOT = "sos_toolkit.tool"

#
###

###
#
ENV_SYSTEM_FILE = "SOS_SYSTEM_FILE"
ENV_LOCAL_FILE = "SOS_LOCAL_FILE"
ENV_USER_FILE = "SOS_USER_FILE"
ENV_ROOT_FILE = "SOS_ROOT_FILE"
ENV_CONTEXT_FILE = "SOS_CONTEXT_FILE"

SYSTEM_FILE = "sos-system.yaml"
USER_FILE = "sos-user.yaml"
LOCAL_FILE = "sos-local.yaml"
ROOT_FILE = "sos-root.yaml"
CONTEXT_FILE = "sos-context.yaml"

#
###