from lemon.context import Context
from lemon.request import Request
from tests.base import BasicTest


class TestContest(BasicTest):
    def test_set_context(self):
        ctx = Context()
        ctx.body = {
            'a': 1,
        }
        ctx.request = Request(url_bytes=b'', headers={}, version='1.1', method=b'GET', transport=None)

        assert ctx.body['a'] == 1
        assert ctx.res.body['a'] == 1
        assert ctx.response.body['a'] == 1
        assert id(ctx.res) == id(ctx.response)
        assert id(ctx.res.body) == id(ctx.body)
        assert id(ctx.request) == id(ctx.req)
