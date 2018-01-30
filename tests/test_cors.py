import pytest

from tests import BasicHttpTestCase


@pytest.mark.asyncio
class TestCors(BasicHttpTestCase):
    async def test_cors(self):
        pass
