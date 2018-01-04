import asyncio
from functools import partial
from inspect import signature

from httptools import HttpRequestParser

from lemon.context import Context
from lemon.exception import HandlerParamsError
from lemon.log import (
    logger,
    error_logger,
)
from lemon.request import Request

try:
    import uvloop as async_loop
except ImportError:
    async_loop = asyncio


class HttpProtocol(asyncio.Protocol):
    def __init__(self, app, loop: async_loop.Loop, handlers: list):
        self.app = app
        self.loop = loop
        self.handlers = handlers

        self.transport = None
        self.ctx = None
        self.url_bytes = b''
        self.headers = dict()
        self.parser = HttpRequestParser(self)

    def connection_made(self, transport):
        logger.debug('connection made')

        self.transport = transport

    def data_received(self, data):
        logger.debug('data received')

        # init context
        self.prepare()

        # enable node.js HTTP parser
        self.parser.feed_data(data)

    # def on_message_begin(self):
    #     logger.debug('on_message_begin')

    def on_url(self, url: bytes):
        logger.debug('on_url : {0}'.format(str(url)))

        self.url_bytes += url

    def on_header(self, name: bytes, value: bytes):
        logger.debug('on_header: name: {0}, value: {1}'.format(name, value))

        self.headers[name.decode().casefold()] = value.decode()

    def on_headers_complete(self):
        logger.debug('on_headers_complete')

        self.ctx.req = Request(
            url_bytes=self.url_bytes,
            headers=self.headers,
            version=self.parser.get_http_version(),
            method=self.parser.get_method().decode(),
            transport=self.transport,
            keep_alive=self.parser.should_keep_alive(),
        )

    def on_body(self, body: bytes):
        self.ctx.req.recv_body(body)

    def on_message_complete(self):
        self.ctx.req.fin_body()

        self.ctx.res.keep_alive = self.ctx.req.keep_alive
        self.ctx.res.keep_alive_timeout = self.ctx.req.keep_alive_timeout

        self.loop.create_task(
            self.exec_handlers(self.handlers)
        )

    async def exec_handlers(self, handlers: list, handler_pos: int = 0):
        if handler_pos >= len(handlers):
            return

        logger.debug('The No.{0} handler started'.format(handler_pos))

        try:
            _handler = handlers[handler_pos]
            _handler_params = signature(_handler).parameters
            if len(_handler_params) == 1:
                await _handler(ctx=self.ctx)
            elif len(_handler_params) == 2:
                await _handler(
                    ctx=self.ctx,
                    nxt=partial(self.exec_handlers, handlers, handler_pos + 1),
                )
            else:
                raise HandlerParamsError
        finally:
            if handler_pos == 0:
                self.write_response()

        logger.debug('The No.{0} handler finished'.format(handler_pos))

    def write_response(self):
        logger.debug('response body : {0}'.format(self.ctx.body))

        try:
            self.transport.write(self.ctx.res.datagram())
        finally:
            if not self.parser.should_keep_alive():
                logger.debug('keep alive closed')
                self.transport.close()
                self.transport = None
            self.cleanup()

    def connection_lost(self, error):
        logger.debug('connection lost')

        super().connection_lost(error)

    def prepare(self):
        self.ctx = Context(app=self.app) if self.ctx is None else self.ctx

    def cleanup(self):
        self.ctx = None
        self.url_bytes = b''
        self.headers = dict()


def serve(app, host, port, handlers):
    logger.info('listen : http://{host}:{port}'.format(
        host=host, port=port,
    ))

    loop = async_loop.new_event_loop()
    asyncio.set_event_loop(loop)

    protocol = HttpProtocol
    handlers = partial(
        protocol,
        app=app,
        loop=loop,
        handlers=handlers,
    )
    server_coroutine = loop.create_server(handlers, host=host, port=port)
    server = loop.run_until_complete(server_coroutine)

    try:
        loop.run_forever()
    except Exception as e:
        error_logger.error(e)
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
