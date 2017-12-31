class BasicException(Exception):
    def __init__(self, msg=None):
        self.msg = msg or self.__class__.__name__

    def __str__(self):
        return str(self.msg)


class HandlerParamsError(BasicException):
    pass
