from lemon.request import Request
from lemon.response import Response


class Context:
    def __init__(self):
        self.body = None
        self.request = self.req = None
        self.response = self.res = Response(body=self.body)

    def set_request(self, request: Request):
        self.request = self.req = request

    def set_response(self, response: Response):
        self.response = self.res = response

    def __setattr__(self, key, value):
        if key == 'body' and 'res' in self.__dict__:
            self.__dict__['res'].body = value

        self.__dict__[key] = value
