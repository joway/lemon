import random
import time
from multiprocessing import Process

import requests

PORTS = set()


class HttpClient:
    def __init__(self):
        self.port = self.random_port()
        self.host = '127.0.0.1'

        self.process = None

    @property
    def base_url(self):
        return 'http://{0}:{1}'.format(
            self.host, self.port,
        )

    def get(self, path, params=None):
        req = requests.get('{0}{1}'.format(self.base_url, path), params=params, headers={'Connection': 'close'})
        req.close()
        return req

    def create_server(self, listen, **kwargs):
        process = Process(target=listen, kwargs=kwargs)
        process.daemon = True
        process.start()
        self.process = process
        time.sleep(0.1)

    def stop_server(self):
        if self.process is not None:
            self.process.terminate()
            while self.process.is_alive():
                time.sleep(0.1)
            PORTS.remove(self.port)

    @staticmethod
    def random_port():
        port = random.randrange(10000, 30000)
        while port in PORTS:
            port = random.randrange(10000, 30000)
        PORTS.add(port)
        return port
