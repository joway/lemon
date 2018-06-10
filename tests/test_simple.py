import pytest

from lemon.context import Context
from tests import BasicHttpTestCase


@pytest.mark.asyncio
class TestSimple(BasicHttpTestCase):
    async def test_simple(self):
        async def handle(ctx: Context):
            ctx.res.body = {
                'msg': ctx.req.data['msg'],
            }

        self.app.use(handle)
        req = await self.post('/', data={
            'msg': 'hi',
        })
        data = req.json()
        assert req.status_code == 200
        assert data['msg'] == 'hi'
