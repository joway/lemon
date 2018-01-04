from lemon.context import Context
from tests.base import HttpBasicTest


class TestMiddleware(HttpBasicTest):
    def test_error_middleware(self):
        async def handle(ctx: Context):
            raise Exception

        client = self.create_http_server([handle])
        req = client.get('/')
        data = req.text
        assert req.status_code == 500
        assert data == 'INTERNAL ERROR'

        client.stop_server()
