from lemon import config
from lemon.server import serve


class Lemon:
    def __init__(self):
        self.host = config.LEMON_SERVER_HOST
        self.port = config.LEMON_SERVER_PORT

    def use(self, handler):
        pass

    def listen(self, host=None, port=None):
        self.host = host or self.host
        self.port = port or self.port
        serve(self.host, self.port)
