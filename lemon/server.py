import typing

import uvicorn

from lemon.log import (
    logger,
)


def serve(app: typing.Callable, host: typing.Text, port: typing.Text or int) -> None:
    """Run server
    :param app: app function
    :param host: eg: "0.0.0.0"
    :param port: eg: 9999
    """
    logger.info('listen : http://{host}:{port}'.format(
        host=host, port=port,
    ))
    uvicorn.run(app, host=host, port=port)
