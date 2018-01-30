import pytest

from lemon.app import Lemon
from lemon.const import HTTP_METHODS
from lemon.context import Context
from lemon.cors import lemon_cors_middleware
from tests import BasicHttpTestCase


@pytest.mark.asyncio
class TestCors(BasicHttpTestCase):
    async def test_cors_simple_request(self):
        async def handle(ctx: Context):
            ctx.body = {
                'ack': 'ok',
            }

        self.app.use(lemon_cors_middleware, handle)
        # GET
        req = await self.asgi_request(
            self.app,
            HTTP_METHODS.GET, '/',
            headers=[
                [b'origin', b'a.com'],
            ]
        )
        assert req.headers['access-control-allow-origin'] == 'a.com'

        # POST
        req = await self.asgi_request(
            self.app,
            HTTP_METHODS.POST, '/',
            headers=[
                [b'origin', b'a.com'],
            ]
        )
        assert req.headers['access-control-allow-origin'] == 'a.com'

        # HEAD
        req = await self.asgi_request(
            self.app,
            HTTP_METHODS.HEAD, '/',
            headers=[
                [b'origin', b'a.com'],
            ]
        )
        assert req.headers['access-control-allow-origin'] == 'a.com'

    async def test_cors_preflight_request(self):
        async def handle(ctx: Context):
            ctx.body = {
                'ack': 'ok',
            }

        self.app.use(lemon_cors_middleware, handle)

        req = await self.asgi_request(
            self.app,
            HTTP_METHODS.OPTIONS, '/',
            headers=[
                [b'origin', b'a.com'],
                [b'access-control-request-method', b'POST'],
                [b'access-control-request-headers', b'X-PINGOTHER, Content-Type'],
            ]
        )
        assert req.headers['access-control-allow-origin'] == 'a.com'
        assert req.headers['access-control-allow-methods'] == 'GET,POST,PUT,DELETE,HEAD,PATCH'
        assert req.headers['access-control-allow-headers'] == 'X-PINGOTHER, Content-Type'

    async def test_cors_config(self):
        async def handle(ctx: Context):
            ctx.body = {
                'ack': 'ok',
            }

        app = Lemon(config={
            'LEMON_CORS_ALLOW_METHODS': ['GET', 'POST'],
            'LEMON_CORS_ALLOW_HEADERS': ['allow_header'],
            'LEMON_CORS_EXPOSE_HEADERS': ['test_header'],
            'LEMON_CORS_ALLOW_CREDENTIALS': True,
            'LEMON_CORS_ORIGIN': '*',
            'LEMON_CORS_MAX_AGE': 8640,
        }, debug=True)
        app.use(lemon_cors_middleware, handle)

        # preflight
        req = await self.asgi_request(
            app,
            HTTP_METHODS.OPTIONS, '/',
            headers=[
                [b'origin', b'a.com'],
                [b'access-control-request-method', b'POST'],
                [b'access-control-request-headers', b'X-PINGOTHER, Content-Type'],
            ]
        )
        assert req.headers['access-control-allow-origin'] == '*'
        assert req.headers['access-control-allow-methods'] == 'GET,POST'
        assert req.headers['access-control-allow-headers'] == 'allow_header'
        assert req.headers['access-control-allow-credentials'] == 'true'
        assert req.headers['access-control-max-age'] == '8640'

        req = await self.asgi_request(
            app,
            HTTP_METHODS.POST, '/',
            headers=[
                [b'origin', b'a.com'],
                [b'x-pingother', b'xxx'],
            ]
        )
        assert req.headers['access-control-allow-origin'] == '*'
        assert req.headers['access-control-allow-credentials'] == 'true'
        assert req.headers['access-control-expose-headers'] == 'test_header'
