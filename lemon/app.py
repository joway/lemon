import logging.config

from lemon import config
from lemon.log import LOGGING_CONFIG_DEFAULTS, logger
from lemon.middleware import lemon_error_handler
from lemon.server import serve

LEMON_MIDDLEWARE_LIST = {
    lemon_error_handler,
}


class Lemon:
    def __init__(self, debug=False):
        self.host = config.LEMON_SERVER_HOST
        self.port = config.LEMON_SERVER_PORT

        self.handlers = []
        self.handlers.extend(LEMON_MIDDLEWARE_LIST)

        # logging
        logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)

    def use(self, handler):
        self.handlers.append(handler)

    def listen(self, host: str = None, port: str = None):
        self.host = host or self.host
        self.port = port or self.port
        serve(self, self.host, self.port, self.handlers)
