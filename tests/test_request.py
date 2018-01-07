import pytest

from lemon.request import Request
from tests.base import BasicTest


@pytest.mark.asyncio
class TestRequest(BasicTest):
    async def test_set_context(self):
        req = await Request.from_asgi_interface({
            'channel': 'http.request',
            'server': ('127.0.0.1', 9999),
            'client': ('127.0.0.1', 58175),
            'scheme': 'http',
            'http_version': '0.0',
            'method': 'POST',
            'path': '/',
            'query_string': b'',
            'headers': [
                [b'content-type', b'application/x-www-form-urlencoded'],
                [b'cache-control', b'no-cache'],
                [b'postman-token', b'e279159d-6af2-45da-87ac-1a331f317a60'],
                [b'user-agent', b'PostmanRuntime/7.1.1'],
                [b'accept', b'*/*'],
                [b'host', b'127.0.0.1:9999'],
                [b'accept-encoding', b'gzip, deflate'],
                [b'content-length', b'11'],
                [b'connection', b'keep-alive'],
            ]
        }, {})
        assert isinstance(req.headers, dict)
        assert req.headers['content-type'] == 'application/x-www-form-urlencoded'
        assert req.host == '127.0.0.1:9999'
        assert req.secure is False
        assert req.protocol == 'http'
        assert req.content_type == 'application/x-www-form-urlencoded'
