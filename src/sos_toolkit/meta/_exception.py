

###
#
class RuntimeBreak(Exception):
    """Raised by a runnable when an action execution should not continue an action list"""
    def __init__(self, message, data=None):
        super().__init__(message)

        self.data = data

#
###