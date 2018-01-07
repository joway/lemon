"""
==========   RuntimeError   ==========
"""


class BasicRuntimeError(RuntimeError):
    def __init__(self, msg=None):
        self.msg = msg or self.__class__.__name__

    def __str__(self):
        return str(self.msg)


class MiddlewareParamsError(BasicRuntimeError):
    pass


class RouterRegisterError(BasicRuntimeError):
    pass


class RouterMatchError(BasicRuntimeError):
    pass


class RequestParserError(BasicRuntimeError):
    pass


class ResponseFormatError(BasicRuntimeError):
    pass


"""
==========   HttpError   ==========
"""


class HttpError(Exception):
    def __init__(self, status: int, body: str or dict):
        self.status = status
        self.body = body
