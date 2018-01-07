import asyncio

import uvicorn

from lemon.log import (
    logger,
)

try:
    import uvloop as async_loop
except ImportError:
    async_loop = asyncio


def serve(app, host, port, handlers):
    logger.info('listen : http://{host}:{port}'.format(
        host=host, port=port,
    ))
    uvicorn.run(app, host=host, port=port)
