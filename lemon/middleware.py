import re
import traceback
import typing

from lemon.config import settings
from lemon.context import Context
from lemon.exception import GeneralException


async def exception_middleware(ctx: Context, nxt: typing.Callable) -> typing.Any:
    """Catch the final exception"""
    try:
        return await nxt()
    except GeneralException as e:
        ctx.body = e.body
        ctx.status = e.status
        if settings.LEMON_DEBUG:
            traceback.print_exc()
    except Exception as e:
        ctx.status = 500
        ctx.body = ctx.body or {
            'error': 'unknown error',
        }
        traceback.print_exc()


async def cors_middleware(ctx: Context, nxt: typing.Callable):
    # settings
    LEMON_CORS_ORIGIN_WHITELIST = settings.LEMON_CORS_ORIGIN_WHITELIST
    LEMON_CORS_ORIGIN_REGEX_WHITELIST = settings.LEMON_CORS_ORIGIN_REGEX_WHITELIST
    LEMON_CORS_ALLOW_METHODS = settings.LEMON_CORS_ALLOW_METHODS
    LEMON_CORS_ALLOW_HEADERS = settings.LEMON_CORS_ALLOW_HEADERS
    LEMON_CORS_EXPOSE_HEADERS = settings.LEMON_CORS_EXPOSE_HEADERS
    LEMON_CORS_ALLOW_CREDENTIALS = settings.LEMON_CORS_ALLOW_CREDENTIALS
    LEMON_CORS_MAX_AGE = settings.LEMON_CORS_MAX_AGE

    if ctx.req is None:
        return

    headers = ctx.req.headers
    origin = headers.get('origin', None)

    # pass request
    if origin is None:
        return await nxt()

    # preflight request
    if ctx.req.method == 'OPTIONS':
        acrm = headers.get('access-control-request-method', None)
        acrh = headers.get('access-control-request-headers', None)
        if acrm is None:
            return await nxt()

        matched = False
        for domain in LEMON_CORS_ORIGIN_WHITELIST:
            if domain == origin:
                matched = True
        for domain_pattern in LEMON_CORS_ORIGIN_REGEX_WHITELIST:
            if re.match(domain_pattern, origin):
                matched = True
        if matched is False:
            ctx.status = 200
            return

        ctx.res.headers['access-control-allow-origin'] = origin

        if LEMON_CORS_ALLOW_CREDENTIALS:
            ctx.res.headers['access-control-allow-credentials'] = 'true'

        ctx.res.headers['access-control-max-age'] = LEMON_CORS_MAX_AGE
        ctx.res.headers['access-control-allow-methods'] = ','.join(LEMON_CORS_ALLOW_METHODS)
        ctx.res.headers['access-control-allow-headers'] = ','.join(LEMON_CORS_ALLOW_HEADERS) or acrh
        # stop request
        ctx.status = 204
        return

    # cross origin request
    ctx.res.headers['access-control-allow-origin'] = origin
    if LEMON_CORS_ALLOW_CREDENTIALS:
        ctx.res.headers['access-control-allow-credentials'] = 'true'
    if LEMON_CORS_EXPOSE_HEADERS:
        ctx.res.headers['access-control-expose-headers'] = ','.join(LEMON_CORS_EXPOSE_HEADERS)

    return await nxt()
