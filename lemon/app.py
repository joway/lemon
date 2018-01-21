import json
import logging.config
import typing
from asyncio import get_event_loop
from functools import partial
from inspect import signature

from lemon.config import settings
from lemon.const import MIME_TYPES
from lemon.context import Context
from lemon.exception import MiddlewareParamsError
from lemon.log import LOGGING_CONFIG_DEFAULTS, logger
from lemon.middleware import lemon_error_middleware
from lemon.request import Request
from lemon.server import serve

LEMON_MIDDLEWARE_LIST = {
    lemon_error_middleware,
}


async def exec_middleware(ctx: Context, middleware_list: list, pos: int = 0) -> typing.Any:
    if pos >= len(middleware_list):
        return
    logger.debug('The No.{0} middleware started'.format(pos))

    try:
        middleware = middleware_list[pos]
        middleware_params = signature(middleware).parameters
        if len(middleware_params) == 1:
            return await middleware(ctx=ctx)
        elif len(middleware_params) == 2:
            return await middleware(
                ctx=ctx,
                nxt=partial(exec_middleware, ctx, middleware_list, pos + 1),
            )
        else:
            raise MiddlewareParamsError
    finally:
        logger.debug('The No.{0} middleware finished'.format(pos))


class Lemon:
    def __init__(self, config: typing.Dict = None, debug=False) -> None:
        """Init app instance
        :param debug: if debug == True , set log level to DEBUG , else is INFO
        """
        self.config = config
        settings.set_config(config=config)

        self.middleware_list = []
        self.middleware_list.extend(LEMON_MIDDLEWARE_LIST)

        # logging
        logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)

    def use(self, *middlewares) -> None:
        """Register middleware into app

        :param middlewares: the chain of the middleware
        """
        self.middleware_list.extend(middlewares)

    @property
    def application(self) -> typing.Callable:
        async def _wrapper(message: typing.Dict, channels: typing.Dict) -> None:
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
                    await exec_middleware(
                        ctx=ctx, middleware_list=self.middleware_list
                    )
                except MiddlewareParamsError as e:
                    await channels['reply'].send({
                        'status': 500,
                        'headers': MIME_TYPES.APPLICATION_JSON,
                        'content': json.dumps({
                            'lemon': 'Your application middleware '
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

    def listen(self, host: str = None, port: str or int = None) -> None:
        """Running server with binding host:port
        """
        _host = host or settings.LEMON_SERVER_HOST
        _port = port or settings.LEMON_SERVER_PORT
        serve(self.application, _host, _port)

    @staticmethod
    def stop() -> None:
        """Stop app's event loop
        """
        get_event_loop().stop()
