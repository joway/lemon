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
from lemon.middleware import exception_middleware, cors_middleware
from lemon.request import Request
from lemon.server import serve

LEMON_PRE_PROCESS_MIDDLEWARE: list = [
    exception_middleware,
]
if settings.LEMON_CORS_ENABLE:
    LEMON_PRE_PROCESS_MIDDLEWARE.append(
        cors_middleware,
    )

LEMON_POST_PROCESS_MIDDLEWARE: list = []


async def exec_middleware(ctx: Context, middleware_list: list, pos: int = 0) -> typing.Any:
    """Exec middleware list
    :param ctx: Context instance
    :param middleware_list: middleware registered on app
    :param pos: the position in middleware_list
    """
    if pos >= len(middleware_list):
        return

    middleware = middleware_list[pos]
    logger.debug(
        'The No.{0} middleware : {1} started'.format(
            pos,
            middleware.__name__,
        )
    )

    try:
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
        logger.debug(
            'The No.{0} middleware : {1} finished'.format(
                pos,
                middleware.__name__,
            )
        )


class Lemon:
    def __init__(self, config: dict = None, debug=False) -> None:
        """Init app instance
        :param config: app config
        :param debug: if debug == True , set log level to DEBUG , else is INFO
        """
        self.config = config
        settings.set_config(config=config)

        self.middleware_list: list = []

        # logging
        logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)

    def use(self, *middleware) -> None:
        """Register middleware into app
        :param middleware: the chain of the middleware
        """
        self.middleware_list.extend(middleware)

    @property
    def application(self) -> typing.Callable:
        async def _wrapper(message: dict, channels: dict) -> typing.Any:
            """
            :param message: is an ASGI message.
            :param channels: is a dictionary of
            """
            if message['channel'] == 'http.request':
                # init context
                ctx = Context()
                # prepare request
                ctx.req = await Request.from_asgi_interface(
                    message=message, channels=channels
                )
                middleware_chain = \
                    LEMON_PRE_PROCESS_MIDDLEWARE \
                    + self.middleware_list \
                    + LEMON_POST_PROCESS_MIDDLEWARE

                try:
                    await exec_middleware(
                        ctx=ctx, middleware_list=middleware_chain
                    )
                except MiddlewareParamsError as e:
                    return await channels['reply'].send({
                        'status': 500,
                        'headers': MIME_TYPES.APPLICATION_JSON,
                        'content': json.dumps({
                            'lemon': 'Your application middleware '
                                     'has wrong num of params',
                        }).encode(),
                    })
                else:
                    return await channels['reply'].send(ctx.res.message)
            # TODO: websocket support
            elif message['channel'] == 'websocket.connect':
                return None
            elif message['channel'] == 'websocket.receive':
                return None
            elif message['channel'] == 'websocket.disconnect':
                return None

        return _wrapper

    def listen(self, host: str = None, port: typing.Union[int, str] = None) -> None:
        """Running server with binding host:port
        :param host: "127.0.0.1"
        :param port: 9999
        """
        _host = host or settings.LEMON_SERVER_HOST
        _port = port or settings.LEMON_SERVER_PORT
        serve(self.application, _host, _port)

    @staticmethod
    def stop() -> None:
        """Stop app's event loop
        """
        get_event_loop().stop()
