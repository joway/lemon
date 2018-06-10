import typing

from werkzeug.datastructures import ImmutableMultiDict

from lemon.parsers import parse_http_body
from lemon.request import Request, HttpHeaders


class ASGIRequest:
    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive: typing.Callable, send: typing.Callable):
        # receive body
        body = b''
        more_body = True
        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)

        # parse headers
        http_headers = HttpHeaders(raw_headers=self.scope['headers'])

        # parse data
        data = parse_http_body(headers=http_headers, body=body) if body else ImmutableMultiDict()

        # create request
        return Request(
            http_version=self.scope['http_version'],
            method=self.scope['method'],
            scheme=self.scope['scheme'],
            path=self.scope['path'],
            query_string=self.scope['query_string'].decode('utf-8'),
            headers=http_headers,
            body=body,
            data=data,
            client=self.scope['client'],
            server=self.scope['server'],
        )
