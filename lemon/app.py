import logging.config
import typing
from asyncio import get_event_loop
from functools import partial
from inspect import signature

from lemon.asgi import ASGIRequest
from lemon.config import settings
from lemon.context import Context
from lemon.exception import LemonMiddlewareParamsError
from lemon.log import LOGGING_CONFIG_DEFAULTS, logger
from lemon.middleware import exception_middleware, cors_middleware
from lemon.server import serve

LEMON_PRE_PROCESS_MIDDLEWARE: list = [
    exception_middleware,
]

LEMON_POST_PROCESS_MIDDLEWARE: list = []


async def exec_middleware(ctx: Context, middleware_list: list, pos: int = 0):
    """Exec middleware list

    :param ctx: Context instance
    :param middleware_list: middleware registered on app
    :param pos: current pos in middleware_list
    """
    if pos >= len(middleware_list):
        return

    middleware = middleware_list[pos]
    logger.debug(
        'middleware : %s started',
        middleware.__name__,
    )

    middleware_params = signature(middleware).parameters
    if len(middleware_params) == 1:
        await middleware(ctx=ctx)
    elif len(middleware_params) == 2:
        return await middleware(
            ctx=ctx,
            nxt=partial(exec_middleware, ctx, middleware_list, pos + 1),
        )
    else:
        raise LemonMiddlewareParamsError


class Lemon:
    def __init__(self, config: dict = None, debug=False) -> None:
        """Init app instance
        :param config: app config
        :param debug: if debug == True , set log level to DEBUG , else is INFO
        """
        settings.set_config(config=config or {})

        self.middleware_list: list = []

        self.pre_process_middleware_list = LEMON_PRE_PROCESS_MIDDLEWARE
        self.post_process_middleware_list = LEMON_POST_PROCESS_MIDDLEWARE
        if settings.LEMON_CORS_ENABLE:
            self.pre_process_middleware_list.append(
                cors_middleware,
            )

        # logging
        logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)

    def use(self, *middleware) -> None:
        """Register middleware into app
        :param middleware: chain of the middleware
        """
        self.middleware_list.extend(middleware)

    @property
    def application(self) -> typing.Callable:
        def _make(scope: dict):
            async def _call(receive: typing.Callable, send: typing.Callable):
                # init context
                ctx = Context()

                # prepare request
                ctx.req = await ASGIRequest(scope)(receive, send)

                middleware_chain = \
                    self.pre_process_middleware_list \
                    + self.middleware_list \
                    + self.post_process_middleware_list

                await exec_middleware(
                    ctx=ctx, middleware_list=middleware_chain,
                )

                await send({
                    'type': 'http.response.start',
                    'status': ctx.res.status,
                    'headers': ctx.res.raw_headers,
                })
                await send({
                    'type': 'http.response.body',
                    'body': ctx.res.raw_body,
                })

            return _call

        return _make

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
