import typing

import uvicorn

from lemon.log import (
    logger,
)


def serve(app: typing.Callable, host: str, port: typing.Union[int, str]) -> None:
    """Run server
    :param app: app function
    :param host: eg: "0.0.0.0"
    :param port: eg: 9999
    """
    logger.info(f'listen : http://{host}:{port}')
    uvicorn.run(app=app, host=host, port=int(port))
