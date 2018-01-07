import uvicorn

from lemon.log import (
    logger,
)


def serve(app, host, port):
    logger.info('listen : http://{host}:{port}'.format(
        host=host, port=port,
    ))
    uvicorn.run(app, host=host, port=port)
