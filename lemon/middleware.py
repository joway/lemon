from lemon.context import Context
from lemon.exception import HttpError
from lemon.log import error_logger


async def lemon_error_middleware(ctx: Context, nxt):
    """Catch the final exception"""
    try:
        await nxt()
    except HttpError as e:
        ctx.body = e.body
        ctx.status = e.status
    except Exception as e:
        error_logger.error(e)
        ctx.status = 500
        ctx.body = ctx.body or 'INTERNAL ERROR'
