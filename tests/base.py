from lemon.app import Lemon
from tests.http import HttpClient


class BasicTest:
    pass


class HttpBasicTest(BasicTest):
    def create_http_server(self, handlers: list):
        client = HttpClient()
        app = Lemon(debug=False)
        app.use(*handlers)
        client.create_server(app.listen, port=client.port)
        return client
