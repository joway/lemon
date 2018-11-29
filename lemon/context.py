import typing

from lemon.exception import GeneralException
from lemon.request import Request
from lemon.response import Response


class Context:
    """The Context object store the current request and response .
    Your can get all information by use ctx in your handler function .
    """

    def __init__(self) -> None:
        self.req: typing.Optional[Request] = None
        self.res: Response = Response()
        # store middleware communication message
        self.state: dict = {}
        self.params: typing.Optional[dict] = None

    def __setattr__(self, key, value) -> None:
        # alias
        if key == 'body':
            self.res.body = value
        elif key == 'status':
            self.res.status = value
        else:
            self.__dict__[key] = value

    def __getattr__(self, item) -> typing.Any:
        # alias
        if item == 'body':
            return self.res.body
        elif item == 'status':
            return self.res.status
        return self.__dict__[item]

    @staticmethod
    def throw(status: int, body: typing.Union[str, dict] = None) -> None:
        """Throw the status and response body"""
        raise GeneralException(status=status, body=body)
