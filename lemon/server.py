import asyncio

try:
    import uvloop as async_loop
except ImportError:
    async_loop = asyncio

from lemon.log import (
    logger,
    error_logger,
)


class HttpProtocol(asyncio.Protocol):
    def __init__(self, connections=set()):
        self.transport = None
        self.connections = connections

    def connection_made(self, transport):
        self.connections.add(self)
        self.transport = transport

    def data_received(self, data):
        self.transport.write(data)

    def eof_received(self):
        if self.transport.can_write_eof():
            self.transport.write_eof()

    def connection_lost(self, error):
        super().connection_lost(error)


def serve(host, port):
    logger.info('listen : http://{host}:{port}'.format(
        host=host, port=port,
    ))
    loop = async_loop.new_event_loop()
    asyncio.set_event_loop(loop)
    server_coroutine = loop.create_server(HttpProtocol, host=host, port=port)
    server = loop.run_until_complete(server_coroutine)

    try:
        loop.run_forever()
    except Exception as e:
        error_logger.error(e)
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
