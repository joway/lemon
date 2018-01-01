from lemon.context import Context
from lemon.exception import HttpError


async def lemon_error_handler(ctx: Context, nxt):
    try:
        await nxt()
    except HttpError as e:
        ctx.body = e.body
        ctx.status = e.status
    except Exception:
        ctx.status = 500
        ctx.body = ctx.body or 'INTERNAL ERROR'
