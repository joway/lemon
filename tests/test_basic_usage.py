import pytest

from lemon.context import Context
from tests import BasicHttpTestCase


@pytest.mark.asyncio
class TestBasicUsage(BasicHttpTestCase):
    async def test_get_json(self):
        async def handle(ctx: Context):
            ctx.body = {
                'ack': 'yeah !',
            }

        self.app.use(handle)
        req = await self.get('/')
        ret = req.json()
        assert req.status_code == 200
        assert ret['ack'] == 'yeah !'

    async def test_get_string(self):
        async def handle(ctx: Context):
            ctx.body = 'xxxxxx'

        self.app.use(handle)
        req = await self.get('/')
        assert req.status_code == 200
        assert req.text == 'xxxxxx'

    async def test_post_json(self):
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

    async def test_post_form(self):
        async def handle(ctx: Context):
            data = ctx.req.json
            ctx.body = {
                'hi': data['hi'],
            }

        self.app.use(handle)
        req = await self.post(path='/', data={
            'hi': 'hello',
        })
        data = req.json()
        assert req.status_code == 200
        assert data['hi'] == 'hello'

    async def test_post_multipart(self):
        async def handle(ctx: Context):
            data = ctx.req.data
            ctx.body = {
                'ack': data['xxx'].read().decode(),
            }

        self.app.use(handle)
        req = await self.asgi_request(
            app=self.app,
            method='POST',
            path='/',
            headers=[
                [b'content-type', b'multipart/form-data; boundary=--------------------------927900071949197777043086']
            ],
            body=b'----------------------------927900071949197777043086\r\nContent-Disposition: form-data; '
                 b'name="xxx"; filename="avatar.jpg"\r\nContent-Type: '
                 b'image/jpeg\r\n\r\n' + 'xxx'.encode() + b'\r\n'
                                                          b'----------------------------927900071949197777043086--\r\n',
        )
        data = req.json()
        assert req.status_code == 200
        assert data['ack'] == 'xxx'

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
        req = await self.options('/')
        assert req.status_code == 200

    async def test_handlers(self):
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

    async def test_cookies(self):
        async def handle(ctx: Context):
            my_cookie = ctx.req.cookies.get('my_cookie')
            my_cookie2 = ctx.req.cookies.get('my_cookie2')
            ctx.body = {
                'my_cookie': my_cookie,
                'my_cookie2': my_cookie2,
            }

        self.app.use(handle)
        req = await self.asgi_request(
            app=self.app,
            method='POST',
            path='/',
            headers=[[
                b'cookie',
                b'my_cookie=xxx; my_cookie2=xxx2'
            ]],
        )
        data = req.json()
        assert req.status_code == 200
        assert data['my_cookie'] == 'xxx'
        assert data['my_cookie2'] == 'xxx2'

    async def test_set_headers(self):
        async def handle(ctx: Context):
            ctx.res.headers['test_headers'] = 'xxx'

        self.app.use(handle)

        req = await self.get('/')
        assert req.status_code == 200
        assert req.headers['test_headers'] == 'xxx'
