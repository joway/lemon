import pytest

from lemon.context import Context
from tests import BasicHttpTestCase


@pytest.mark.asyncio
class TestApp(BasicHttpTestCase):
    async def test_json_response(self):
        async def handle(ctx: Context):
            ctx.body = {
                'ack': 'yeah !',
            }

        self.app.use(handle)
        req = await self.get('/')
        ret = req.json()
        assert req.status_code == 200
        assert ret['ack'] == 'yeah !'

    async def test_string_response(self):
        async def handle(ctx: Context):
            ctx.body = 'xxxxxx'

        self.app.use(handle)
        req = await self.get('/')
        assert req.status_code == 200
        assert req.text == 'xxxxxx'

    async def test_json_post(self):
        async def handle(ctx: Context):
            ctx.body = ctx.req.json

        self.app.use(handle)
        req = await self.post('/', data={
            'int': 1,
            'str': 'xxx'
        })
        assert req.status_code == 200
        data = req.json()
        assert data['int'] == 1
        assert data['str'] == 'xxx'

    async def test_other_method(self):
        async def handle(ctx: Context):
            ctx.body = {
                'ack': 'yeah !',
            }

        self.app.use(handle)
        req = await self.post('/')
        data = req.json()
        assert req.status_code == 200
        assert data['ack'] == 'yeah !'
        req = await self.delete('/')
        data = req.json()
        assert req.status_code == 200
        assert data['ack'] == 'yeah !'
        req = await self.put('/')
        data = req.json()
        assert req.status_code == 200
        assert data['ack'] == 'yeah !'

    async def test_throw(self):
        async def handle(ctx: Context):
            raise Exception

        self.app.use(handle)
        req = await self.get('/')
        assert req.status_code == 500

    async def test_middleware_and_handler(self):
        async def middleware(ctx: Context, nxt):
            ctx.body = {
                'msg': 'hello world'
            }
            await nxt()

        async def handle(ctx: Context):
            ctx.body['ack'] = 'yeah !'
            ctx.body['int'] = 1

        self.app.use(middleware, handle)
        req = await self.get('/')
        data = req.json()
        assert req.status_code == 200
        assert data['msg'] == 'hello world'
        assert data['ack'] == 'yeah !'
        assert data['int'] == 1

    async def test_custom_error_middleware(self):
        async def err_middleware(ctx: Context, nxt):
            ctx.body = {
                'msg': 'err_middleware'
            }
            try:
                await nxt()
            except Exception:
                ctx.body = {
                    'msg': 'error handled'
                }
                ctx.status = 400

        async def handle(ctx: Context):
            raise Exception('error')

        self.app.use(err_middleware, handle)
        req = await self.get('/')
        data = req.json()
        assert req.status_code == 400
        assert data['msg'] == 'error handled'
