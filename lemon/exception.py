import typing


class GeneralException(BaseException):
    def __init__(self, status=None, body: typing.Union[str, dict] = None) -> None:
        self.status = status
        self.body = body


# ==========   RequestException 4xx  ==========
class RequestBadError(GeneralException):
    def __init__(self):
        super().__init__(status=400, body={
            'error': 'bad request'
        })


class RequestUnauthorizedError(GeneralException):
    def __init__(self):
        super().__init__(status=401, body={
            'error': 'unauthorized'
        })


class RequestForbiddenError(GeneralException):
    def __init__(self):
        super().__init__(status=403, body={
            'error': 'not found'
        })


class RequestNotFoundError(GeneralException):
    def __init__(self):
        super().__init__(status=404, body={
            'error': 'not found'
        })


class RequestHeadersParserError(RequestBadError):
    pass


class RequestBodyParserError(RequestBadError):
    pass


# ==========   RuntimeError - 5xx  ==========
class ServerError(GeneralException):
    def __init__(self):
        super().__init__(status=500, body={
            'error': 'internal error'
        })


class LemonMiddlewareParamsError(ServerError):
    pass


class LemonRouterRegisterError(ServerError):
    pass


class LemonRouterMatchError(ServerError):
    pass


class LemonConfigKeyError(ServerError):
    pass
