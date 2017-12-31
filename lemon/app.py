from lemon import config


class Lemon:
    def __init__(self):
        self.host = config.LEMON_SERVER_HOST
        self.port = config.LEMON_SERVER_PORT

    def use(self, handler):
        pass

    def listen(self, port=None):
        if port:
            self.port = port
