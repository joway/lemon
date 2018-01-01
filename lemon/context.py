from lemon.exception import HttpError
from lemon.response import Response


class Context:
    def __init__(self, app):
        self.app = app

        self.req = None
        self.res = Response()
        self.state = {}

    def __setattr__(self, key, value):
        if key == 'body':
            self.res.body = value
        if key == 'status':
            self.res.status = value
        else:
            self.__dict__[key] = value

    def __getattr__(self, item):
        # alias
        if item == 'body':
            return self.res.body
        if item == 'status':
            return self.res.status
        return self.__dict__[item]

    def throw(self, status: int, body: str or dict = None):
        raise HttpError(status=status, body=body)
