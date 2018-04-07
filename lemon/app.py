import asyncio
import json
import logging.config
import time
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
from lemon.wsconnection import WSConnection, WSMessage

LEMON_PRE_PROCESS_MIDDLEWARE: list = [
    exception_middleware,
]

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


# websocket: empty handler
async def empty_handler(*args, **kwargs):
    pass


class Lemon:
    def __init__(self, config: dict = None, debug=False) -> None:
        """Init app instance
        :param config: app config
        :param debug: if debug == True , set log level to DEBUG , else is INFO
        """
        self.config = config
        settings.set_config(config=config)

        self.middleware_list: list = []
        self.pre_process_middleware_list = LEMON_PRE_PROCESS_MIDDLEWARE
        self.post_process_middleware_list = LEMON_POST_PROCESS_MIDDLEWARE
        if settings.LEMON_CORS_ENABLE:
            self.pre_process_middleware_list.append(
                cors_middleware,
            )

        # websocket
        self.ws_enable = False
        self.ws_pull = None
        self.ws_push = None
        self.ws_conns = set()

        # logging
        logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)

    def ws(self, ws_pull: typing.Callable, ws_push: typing.Callable):
        """Register pull and push handlers for websocket connections
        :param ws_pull: handler function to pull from server
        :param ws_push: handler function to push to client
        """
        self.ws_enable = True
        self.ws_pull = ws_pull
        self.ws_push = ws_push

    def use(self, *middleware) -> None:
        """Register middleware into app
        :param middleware: the chain of the middleware
        """
        self.middleware_list.extend(middleware)

    @property
    def application(self) -> typing.Callable:
        # websocket enable : push message to client
        # if self.ws_enable:
        #     # TODO: auto timeout connection
        #     pass
        #
        #     # push daemon
        #     asyncio.ensure_future(self.ws_push(self.ws_conns))

        async def _wrapper(message: dict, channels: dict) -> typing.Any:
            """
            :param message: is an ASGI message.
            :param channels: is a dictionary of
            """
            if message['channel'] == 'http.request':
                # init context
                ctx = Context()
                # prepare HTTP request
                ctx.req = await Request.from_asgi_interface(
                    message=message, channels=channels
                )
                middleware_chain = \
                    self.pre_process_middleware_list \
                    + self.middleware_list \
                    + self.post_process_middleware_list

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

            # websocket connection
            ws_conn = WSConnection(channels['reply']._websocket)
            if message['channel'] == 'websocket.connect':
                await ws_conn.establish()
                self.ws_conns.add(ws_conn)
                logger.info(f'Websocket connected')
            # disconnect
            elif message['channel'] == 'websocket.disconnect':
                try:
                    self.ws_conns.remove(ws_conn)
                except:
                    pass
                await ws_conn.destroy()
                logger.info(f'Websocket disconnected')
            # receive msg from client
            elif message['channel'] == 'websocket.receive':
                ws_msg = WSMessage(message)
                await self.ws_pull(ws_conn, ws_msg)
                logger.info(f'Websocket receive message')

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
