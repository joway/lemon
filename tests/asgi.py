import json

from lemon.app import Lemon
from lemon.const import HTTP_METHODS
from lemon.request import HttpHeaders


class ASGIResponse:
    def __init__(self, status, headers: HttpHeaders, content):
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
    app = None
    scope = {}
    address = '127.0.0.1'
    port = 9999

    def setup_method(self, method):
        self.app = Lemon(
            config={
                'LEMON_CORS_ENABLE': True,
            },
            debug=True
        )
        self.scope = {
            'type': 'http.request',
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

    def set_scope(self, method, path, query_string='', headers=None):
        self.scope['method'] = method
        self.scope['path'] = path
        self.scope['query_string'] = query_string.encode('utf-8')

        if headers:
            self.scope['headers'].extend(headers)

    async def asgi_request(
            self, app, method, path, query_string='',
            data=None, body=None, headers=None,
    ):
        raw_body = body or b''
        is_start = False
        resp = {}

        if data:
            raw_body = json.dumps(data).encode()

        _headers = headers or []
        _headers.append(
            [b'content-length', f'{len(raw_body)}'.encode()],
        )
        self.set_scope(method, path, query_string, _headers)

        async def receive():
            return {
                'body': raw_body,
            }

        async def send(msg):
            global is_start
            if msg['type'] == 'http.response.start':
                resp['status'] = msg['status']
                resp['headers'] = msg['headers']
                is_start = True
            if msg['type'] == 'http.response.body':
                assert is_start is True
                resp['body'] = msg['body']

        await app.application(self.scope)(receive, send)
        return ASGIResponse(resp['status'], HttpHeaders(raw_headers=resp['headers']), resp['body'])

    async def get(self, path, params=None):
        query_string = ''
        if params:
            params_pairs = []
            for p in params:
                params_pairs.append('{0}={1}'.format(p, params[p]))
            query_string = '&'.join(params_pairs)

        return await self.asgi_request(
            app=self.app,
            method=HTTP_METHODS.GET,
            path=path,
            query_string=query_string,
        )

    async def post(self, path, data=None):
        return await self.asgi_request(
            app=self.app,
            method=HTTP_METHODS.POST,
            path=path,
            data=data,
        )

    async def put(self, path, data=None):
        return await self.asgi_request(
            app=self.app,
            method=HTTP_METHODS.PUT,
            path=path,
            data=data,
        )

    async def delete(self, path, data=None):
        return await self.asgi_request(
            app=self.app,
            method=HTTP_METHODS.DELETE,
            path=path,
            data=data,
        )

    async def options(self, path, data=None):
        return await self.asgi_request(
            app=self.app,
            method=HTTP_METHODS.OPTIONS,
            path=path,
            data=data,
        )
