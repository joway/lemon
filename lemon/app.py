import json
import logging.config
from asyncio import get_event_loop
from functools import partial
from inspect import signature

from lemon import config
from lemon.const import MIME_TYPES
from lemon.context import Context
from lemon.exception import HandlerParamsError
from lemon.log import LOGGING_CONFIG_DEFAULTS, logger
from lemon.middleware import lemon_error_handler
from lemon.request import Request
from lemon.server import serve

LEMON_MIDDLEWARE_LIST = {
    lemon_error_handler,
}


async def exec_handlers(ctx: Context, handlers: list, handler_pos: int = 0):
    if handler_pos >= len(handlers):
        return

    logger.debug('The No.{0} handler started'.format(handler_pos))

    try:
        _handler = handlers[handler_pos]
        _handler_params = signature(_handler).parameters
        if len(_handler_params) == 1:
            await _handler(ctx=ctx)
        elif len(_handler_params) == 2:
            await _handler(
                ctx=ctx,
                nxt=partial(exec_handlers, ctx, handlers, handler_pos + 1),
            )
        else:
            raise HandlerParamsError
    finally:
        logger.debug('The No.{0} handler finished'.format(handler_pos))


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

    @property
    def application(self):
        async def _wrapper(message, channels):
            """
            :param message: is an ASGI message.
            :param channels: is a dictionary of
             <unicode string>:<channel interface>.
            :return: asgi application
            """
            if message['channel'] == 'http.request':
                # init context
                ctx = Context()
                # prepare request
                ctx.req = await Request.from_asgi_interface(
                    message=message, channels=channels
                )
                try:
                    await exec_handlers(ctx=ctx, handlers=self.handlers)
                except HandlerParamsError as e:
                    await channels['reply'].send({
                        'status': 500,
                        'headers': MIME_TYPES.APPLICATION_JSON,
                        'content': json.dumps({
                            'lemon': 'Your application handler '
                                     'has wrong num of params',
                        }),
                    })
                except Exception as e:
                    logger.error(e)
                    await channels['reply'].send({
                        'status': 500,
                        'headers': MIME_TYPES.APPLICATION_JSON,
                        'content': json.dumps({
                            'lemon': 'INTERNAL ERROR',
                        }),
                    })
                else:
                    await channels['reply'].send(ctx.res.message)
            # TODO: websocket support
            elif message['channel'] == 'websocket.connect':
                pass
            elif message['channel'] == 'websocket.receive':
                pass
            elif message['channel'] == 'websocket.disconnect':
                pass

        return _wrapper

    def listen(self, host: str = None, port: str or int = None):
        """Running server with binding host:port
        """
        self.host = host or self.host
        self.port = str(port or self.port)
        serve(self.application, self.host, self.port, self.handlers)

    def stop(self):
        """Stop app's event loop
        """
        get_event_loop().stop()
