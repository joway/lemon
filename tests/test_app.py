from lemon.context import Context
from tests.base import HttpBasicTest


class TestApp(HttpBasicTest):
    def test_json_response(self):
        async def handle(ctx: Context):
            ctx.body = {
                'ack': 'yeah !',
            }

        client = self.create_http_server([handle])
        req = client.get('/')
        data = req.json()
        assert req.status_code == 200
        assert data['ack'] == 'yeah !'

        client.stop_server()

    def test_string_response(self):
        async def handle(ctx: Context):
            ctx.body = 'xxxxxx'

        client = self.create_http_server([handle])
        req = client.get('/')
        assert req.status_code == 200
        assert req.text == 'xxxxxx'

        client.stop_server()

    def test_throw(self):
        async def handle(ctx: Context):
            raise Exception

        client = self.create_http_server([handle])
        req = client.get('/')
        assert req.status_code == 500

        client.stop_server()

    def test_middleware_and_handler(self):
        async def middleware(ctx: Context, nxt):
            ctx.body = {
                'msg': 'hello world'
            }
            await nxt()

        async def handle(ctx: Context):
            ctx.body['ack'] = 'yeah !'
            ctx.body['int'] = 1

        client = self.create_http_server([middleware, handle])
        req = client.get('/')
        data = req.json()
        assert req.status_code == 200
        assert data['msg'] == 'hello world'
        assert data['ack'] == 'yeah !'
        assert data['int'] == 1
        client.stop_server()

    def test_custom_error_middleware(self):
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

        client = self.create_http_server([err_middleware, handle])
        req = client.get('/')
        data = req.json()
        assert req.status_code == 400
        assert data['msg'] == 'error handled'
        client.stop_server()
