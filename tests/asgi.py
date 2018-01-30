import json
import typing

from lemon.app import Lemon
from lemon.const import HTTP_METHODS


class MockReplyChannel:
    @staticmethod
    async def send(message):
        return message


class MockBodyChannel:
    def __init__(self, mock_data: typing.Dict):
        self.message = {
            'content': json.dumps(mock_data).encode('utf-8'),
        }

    async def receive(self):
        return self.message


class ASGIRequest:
    def __init__(self, status, headers, content):
        self.status = status
        self.headers = headers
        self.content = content

    @property
    def status_code(self):
        return self.status

    @property
    def text(self):
        return self.content.decode('utf-8')

    def json(self):
        return json.loads(self.content)


class ASGIHttpTestCase:
    address = '127.0.0.1'
    port = 9999

    def setup_method(self, method):
        self.app = Lemon(debug=True)

        self.message = {
            'channel': 'http.request',
            'server': (self.address, self.port),
            'client': ('127.0.0.1', 55555),
            'scheme': 'http',
            'http_version': '1.1',
            'headers': [
                [b'user-agent', b'lemon-pytest'],
                [b'accept', b'*/*'],
                [b'host', '{0}:{1}'.format(self.address, self.port).encode()],
                [b'connection', b'keep-alive'],
            ],
        }

        self.channels = {
            'reply': MockReplyChannel()
        }

    def mock_asgi_message(self, method, path, query_string='', data=None):
        self.message['method'] = method
        self.message['path'] = path
        self.message['query_string'] = query_string.encode('utf-8')
        if data:
            self.message['headers'].extend([
                [b'content-type', b'application/json'],
                [b'content-length', bytes(len(json.dumps(data)))],
            ])
            self.channels['body'] = MockBodyChannel(mock_data=data)

    async def asgi_request(self, method, path, query_string='', data=None):
        self.mock_asgi_message(method, path, query_string, data)
        req = await self.app.application(self.message, self.channels)
        return ASGIRequest(req['status'], req['headers'], req['content'])

    async def get(self, path, params=None):
        query_string = ''
        if params:
            query_string = '?'
            params_pairs = []
            for p in params:
                params_pairs.append('{0}={1}'.format(p, params[p]))
            query_string += '&'.join(params)

        return await self.asgi_request(
            method=HTTP_METHODS.GET,
            path=path,
            query_string=query_string,
        )

    async def post(self, path, data=None):
        return await self.asgi_request(
            method=HTTP_METHODS.POST,
            path=path,
            data=data,
        )

    async def put(self, path, data=None):
        return await self.asgi_request(
            method=HTTP_METHODS.PUT,
            path=path,
            data=data,
        )

    async def delete(self, path, data=None):
        return await self.asgi_request(
            method=HTTP_METHODS.DELETE,
            path=path,
            data=data,
        )
