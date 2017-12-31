from lemon import config
from lemon.server import serve


class Lemon:
    def __init__(self):
        self.host = config.LEMON_SERVER_HOST
        self.port = config.LEMON_SERVER_PORT
        self.request_handlers = []

    def use(self, handler):
        self.request_handlers.append(handler)

    def listen(self, host: str = None, port: str = None):
        self.host = host or self.host
        self.port = port or self.port
        serve(self.host, self.port, self.request_handlers)
