from multiprocessing import Process
from time import sleep

import requests

from lemon.context import Context
from tests import BasicHttpTestCase


class TestServer(BasicHttpTestCase):
    def test_serve(self):
        async def handle(ctx: Context):
            ctx.res.body = {
                'msg': 'hi',
            }

        self.app.use(handle)

        p = Process(target=self.app.listen, args=('127.0.0.1', 9998))
        p.start()
        sleep(1)

        ret = requests.get('http://127.0.0.1:9998')
        data = ret.json()
        assert data['msg'] == 'hi'
        self.app.stop()
        p.terminate()
