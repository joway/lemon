from lemon.response import Response


class Context:
    def __init__(self):
        self.req = None
        self.res = Response()

    def __setattr__(self, key, value):
        if key == 'body':
            self.res.body = value
        elif key == 'request':
            self.req = value
        elif key == 'response':
            self.res = value
        else:
            self.__dict__[key] = value

    def __getattr__(self, item):
        # alias
        if item == 'body':
            return self.res.body

        if item == 'request':
            return self.req

        if item == 'response':
            return self.res
