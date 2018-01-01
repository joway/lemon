import pytest

from lemon.context import Context
from tests.base import HttpBasicTest


class TestApp(HttpBasicTest):
    @pytest.mark.serial
    def test_json_response(self):
        async def handle(ctx: Context):
            ctx.body = {
                'ack': 'yeah !',
            }

        client = self.create_http_server([handle])

        req = client.get('/')
        data = req.json()
        assert data['ack'] == 'yeah !'

        client.stop_server()

    @pytest.mark.serial
    def test_string_response(self):
        async def handle(ctx: Context):
            ctx.body = 'xxxxxx'

        client = self.create_http_server([handle])

        req = client.get('/')
        assert req.text == 'xxxxxx'

        client.stop_server()
