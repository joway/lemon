import typing

from lemon.config import settings
from lemon.context import Context


async def lemon_cors_middleware(ctx: Context, nxt: typing.Callable):
    # settings
    LEMON_CORS_ORIGIN = settings.LEMON_CORS_ORIGIN
    LEMON_CORS_ALLOW_METHODS = settings.LEMON_CORS_ALLOW_METHODS
    LEMON_CORS_ALLOW_HEADERS = settings.LEMON_CORS_ALLOW_HEADERS
    LEMON_CORS_EXPOSE_HEADERS = settings.LEMON_CORS_EXPOSE_HEADERS
    LEMON_CORS_ALLOW_CREDENTIALS = settings.LEMON_CORS_ALLOW_CREDENTIALS
    LEMON_CORS_MAX_AGE = settings.LEMON_CORS_MAX_AGE

    headers = ctx.req.headers
    origin = LEMON_CORS_ORIGIN or headers.get('origin', None)

    # pass request
    if origin is None:
        return await nxt()

    # preflight request
    if ctx.req.method == 'OPTIONS':
        acrm = headers.get('access-control-request-method', None)
        acrh = headers.get('access-control-request-headers', None)
        if acrm is None:
            return await nxt()

        ctx.res.headers['access-control-allow-origin'] = origin

        if LEMON_CORS_ALLOW_CREDENTIALS:
            ctx.res.headers['access-control-allow-credentials'] = 'true'

        ctx.res.headers['access-control-max-age'] = LEMON_CORS_MAX_AGE
        ctx.res.headers['access-control-allow-methods'] = ','.join(LEMON_CORS_ALLOW_METHODS)
        ctx.res.headers['access-control-allow-headers'] = ','.join(LEMON_CORS_ALLOW_HEADERS) or acrh
        ctx.status = 204
        # stop request
        return

    # cross origin request
    ctx.res.headers['access-control-allow-origin'] = origin
    if LEMON_CORS_ALLOW_CREDENTIALS:
        ctx.res.headers['access-control-allow-credentials'] = 'true'
    if LEMON_CORS_EXPOSE_HEADERS:
        ctx.res.headers['access-control-expose-headers'] = ','.join(LEMON_CORS_EXPOSE_HEADERS)

    return await nxt()
