from io import BytesIO

import pytest

from lemon.context import Context
from tests import BasicHttpTestCase


@pytest.mark.asyncio
class TestPostBody(BasicHttpTestCase):
    async def test_json(self):
        async def handle(ctx: Context):
            data = ctx.req.json
            ctx.body = {
                'hi': data['hi'],
            }

        self.app.use(handle)
        req = await self.post(path='/', data={
            'hi': 'hello'
        })
        data = req.json()
        assert req.status_code == 200
        assert data['hi'] == 'hello'

    async def test_form(self):
        async def handle(ctx: Context):
            data = ctx.req.json
            ctx.body = {
                'hi': data['hi'],
            }

        self.app.use(handle)
        req = await self.post(path='/', data={
            'hi': 'hello'
        })
        data = req.json()
        assert req.status_code == 200
        assert data['hi'] == 'hello'

    # async def test_post_multipart(self):
    #     async def handle(ctx: Context):
    #         data = ctx.req.data
    #         ctx.body = {
    #             'ack': data['file'].read().decode(),
    #         }
    #
    #     self.app.use(handle)
    #     req = await self.post(path='/', files={
    #         'file': BytesIO(b'xxxxxx')
    #     })
    #     data = req.json()
    #     assert req.status_code == 200
    #     assert data['ack'] == 'xxxxxx'
