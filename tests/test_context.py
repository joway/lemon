from lemon.context import Context
from lemon.request import Request
from tests.base import BasicTest


class TestContext(BasicTest):
    def test_set_context(self):
        ctx = Context()
        ctx.body = {
            'a': 1,
        }
        ctx.req = Request.from_asgi_interface({
            'channel': 'http.request', 'server': ('127.0.0.1', 9999), 'client': ('127.0.0.1', 58175), 'scheme': 'http',
            'http_version': '0.0', 'method': 'POST', 'path': '/', 'query_string': b'',
            'headers': [[b'content-type', b'application/x-www-form-urlencoded'], [b'cache-control', b'no-cache'],
                        [b'postman-token', b'e279159d-6af2-45da-87ac-1a331f317a60'],
                        [b'user-agent', b'PostmanRuntime/7.1.1'], [b'accept', b'*/*'], [b'host', b'127.0.0.1:9999'],
                        [b'accept-encoding', b'gzip, deflate'], [b'content-length', b'11'],
                        [b'connection', b'keep-alive']]
        }, None)

        assert ctx.body['a'] == 1
        assert ctx.res.body['a'] == 1
        assert id(ctx.res.body) == id(ctx.body)
        assert id(ctx.res.status) == id(ctx.status)
