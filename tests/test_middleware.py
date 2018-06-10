import pytest

from lemon.context import Context
from tests import BasicHttpTestCase


@pytest.mark.asyncio
class TestMiddleware(BasicHttpTestCase):
    async def test_exception_middleware(self):
        async def handle(ctx: Context):
            raise Exception

        self.app.use(handle)
        req = await self.get('/')
        data = req.json()
        assert req.status_code == 500
        assert data['lemon'] == 'INTERNAL ERROR'
