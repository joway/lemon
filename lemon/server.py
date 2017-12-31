import asyncio
from functools import partial
from inspect import signature

from lemon.context import Context
from lemon.exception import HandlerParamsError

try:
    import uvloop as async_loop
except ImportError:
    async_loop = asyncio

from lemon.log import (
    logger,
    error_logger)


class HttpProtocol(asyncio.Protocol):
    def __init__(self, request_handlers: list):
        self.transport = None
        self.request_handlers = request_handlers
        self.ctx = Context()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.ctx.set('body', data)
        self.exec_handler(self.request_handlers)

    def eof_received(self):
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        super().connection_lost(error)

    def exec_handler(self, handlers: list):
        try:
            _handler = handlers.pop(0)
            _handler_params = signature(_handler).parameters
            if 'ctx' in _handler_params:
                if 'nxt' in _handler_params:
                    _handler(ctx=self.ctx, nxt=partial(self.exec_handler, request_handlers))
                else:
                    _handler(ctx=self.ctx)
            else:
                raise HandlerParamsError
        except IndexError:
            return


def serve(host, port, request_handlers):
    logger.info('listen : http://{host}:{port}'.format(
        host=host, port=port,
    ))
    loop = async_loop.new_event_loop()
    asyncio.set_event_loop(loop)

    protocol = HttpProtocol
    handlers = partial(
        protocol,
        request_handlers=request_handlers,
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
