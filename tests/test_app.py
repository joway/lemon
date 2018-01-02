from lemon.context import Context
from tests.base import HttpBasicTest


class TestApp(HttpBasicTest):
    def test_json_response(self):
        print('test_json_response start')

        async def handle(ctx: Context):
            ctx.body = {
                'ack': 'yeah !',
            }

        client = self.create_http_server([handle])

        req = client.get('/')
        data = req.json()
        assert data['ack'] == 'yeah !'

        client.stop_server()

        print('test_json_response stop')

    def test_string_response(self):
        print('test_string_response start')

        async def handle(ctx: Context):
            ctx.body = 'xxxxxx'

        client = self.create_http_server([handle])

        req = client.get('/')
        assert req.text == 'xxxxxx'

        client.stop_server()
        print('test_string_response stop')
