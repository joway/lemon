import logging.config
from asyncio import get_event_loop

from lemon import config
from lemon.log import LOGGING_CONFIG_DEFAULTS, logger
from lemon.middleware import lemon_error_handler
from lemon.server import serve

LEMON_MIDDLEWARE_LIST = {
    lemon_error_handler,
}


class Lemon:
    def __init__(self, debug=False):
        """Init app instance
        :param debug: if debug == True , set log level to DEBUG , else is INFO
        """
        self.host = config.LEMON_SERVER_HOST
        self.port = config.LEMON_SERVER_PORT

        self.handlers = []
        self.handlers.extend(LEMON_MIDDLEWARE_LIST)

        # logging
        logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)

    def use(self, *handlers):
        """Register handlers into app

        :param handlers: the chain of the handlers
        """
        self.handlers.extend(handlers)

    def listen(self, host: str = None, port: str or int = None):
        """Running server with binding host:port
        """
        self.host = host or self.host
        self.port = str(port or self.port)
        serve(self, self.host, self.port, self.handlers)

    def stop(self):
        """Stop app's event loop
        """
        get_event_loop().stop()
