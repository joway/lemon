# ==========   GeneralException  ==========
import typing


class GeneralException(BaseException):
    def __init__(self, status=None, body: typing.Union[str, dict] = None) -> None:
        self.status = status
        self.body = body


# ==========   RuntimeError - 500  ==========
class ServerError(GeneralException):
    def __init__(self, *args, **kwargs) -> None:
        super(ServerError, self).__init__(*args, **kwargs)
        self.status = 500


class MiddlewareParamsError(ServerError):
    pass


class RouterRegisterError(ServerError):
    pass


class RouterMatchError(ServerError):
    pass


class ResponseFormatError(ServerError):
    pass


class LemonConfigKeyError(ServerError):
    pass


# ==========   BadRequestError - 400  ==========
class BadRequestError(GeneralException):
    def __init__(self, *args, **kwargs) -> None:
        super(BadRequestError, self).__init__(*args, **kwargs)
        self.status = 400


class RequestHeadersParserError(BadRequestError):
    pass


class RequestBodyParserError(BadRequestError):
    pass
