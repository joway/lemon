import typing

from lemon.context import Context
from lemon.exception import GeneralException
from lemon.log import error_logger


async def lemon_error_middleware(ctx: Context, nxt) -> typing.Any:
    """Catch the final exception"""
    try:
        return await nxt()
    except GeneralException as e:
        ctx.body = e.body
        ctx.status = e.status
    except Exception as e:
        error_logger.error(e)
        ctx.status = 500
        ctx.body = ctx.body or 'INTERNAL ERROR'
