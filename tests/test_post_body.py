from io import BytesIO

from lemon.context import Context
from tests.base import HttpBasicTest


class TestPostBody(HttpBasicTest):
    def test_json(self):
        async def handle(ctx: Context):
            data = ctx.req.json
            ctx.body = {
                'hi': data['hi'],
            }

        client = self.create_http_server([handle])
        req = client.post(path='/', json={
            'hi': 'hello'
        })
        data = req.json()
        assert req.status_code == 200
        assert data['hi'] == 'hello'

        client.stop_server()

    def test_form(self):
        async def handle(ctx: Context):
            data = ctx.req.json
            ctx.body = {
                'hi': data['hi'],
            }

        client = self.create_http_server([handle])
        req = client.post(path='/', data={
            'hi': 'hello'
        })
        data = req.json()
        assert req.status_code == 200
        assert data['hi'] == 'hello'

        client.stop_server()

    def test_post_multipart(self):
        async def handle(ctx: Context):
            data = ctx.req.data
            ctx.body = {
                'ack': data['file'].read().decode(),
            }

        client = self.create_http_server([handle])
        req = client.post(path='/', files={
            'file': BytesIO(b'xxxxxx')
        })
        data = req.json()
        assert req.status_code == 200
        assert data['ack'] == 'xxxxxx'

        client.stop_server()
