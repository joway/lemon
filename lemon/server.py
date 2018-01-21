import typing

import uvicorn

from lemon.log import (
    logger,
)


def serve(app: typing.Callable, host: typing.Text, port: typing.Text or int) -> None:
    logger.info('listen : http://{host}:{port}'.format(
        host=host, port=port,
    ))
    uvicorn.run(app, host=host, port=port)
