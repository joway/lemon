import typing
from urllib.parse import parse_qs

from werkzeug.datastructures import ImmutableMultiDict

from lemon.const import MIME_TYPES
from lemon.parsers import parse_http_body


class Request:
    """The Request object store the current request's fully information

    Example usage:
            ctx.req
    """

    def __init__(
            self,
            http_version: '1.1',
            method: 'GET',
            scheme: 'https',
            path: '/',
            query_string: b'?k=v',
            headers: typing.Dict,
            body: bytes,
            data: ImmutableMultiDict or None,
            client: ('1.1.1.1', '56938'),
            server: ('127.0.0.1', '9999'),
    ) -> None:
        self.http_version = http_version
        self.method = method.upper()
        self.scheme = scheme
        self.path = path
        self.query_string = query_string
        self.headers = headers
        self.body = body
        self.data = data
        self.client = client
        self.server = server

        # for cache
        self._json = None
        self._query = None

    @property
    def protocol(self) -> typing.Text:
        """http or https
        """
        return self.scheme

    @property
    def secure(self) -> bool:
        """is using https protocol
        """
        return self.scheme == 'https'

    @property
    def host(self) -> typing.Text:
        """HTTP_HEADERS['Host']
        """
        return self.headers.get('host', '')

    @property
    def content_type(self) -> typing.Text:
        """HTTP_HEADERS['Content-Type']
        """
        return self.headers.get('content-type', MIME_TYPES.TEXT_PLAIN)

    @property
    def query(self) -> typing.Dict:
        if self._query is None:
            _q = parse_qs(self.query_string)
            self._query = {k: _q[k][0] for k in _q}
        return self._query

    @property
    def form(self) -> ImmutableMultiDict:
        return self.data

    @property
    def json(self) -> typing.Dict:
        """Transform request body to dict when content_type is 'application/json'
        :return: dict
        """
        return self.data.to_dict(flat=True) if self.data else None

    @classmethod
    async def read_body(cls, message, channels) -> bytes:
        """
        Read and return the entire body from an incoming ASGI message.
        """
        body = message.get('body', b'')
        if 'body' in channels:
            while True:
                message_chunk = await channels['body'].receive()
                body += message_chunk['content']
                if not message_chunk.get('more_content', False):
                    break
        return body

    @classmethod
    async def from_asgi_interface(cls, message, channels) -> typing.Any:
        body = await cls.read_body(message, channels)

        # decode headers
        headers_dict = {}
        for h in message['headers']:
            headers_dict[h[0].decode().lower()] = h[1].decode()
        headers_dict = headers_dict

        # parse body
        parsed_body = parse_http_body(headers=headers_dict, body=body)

        # create request
        return Request(
            http_version=message['http_version'],
            method=message['method'],
            scheme=message['scheme'],
            path=message['path'],
            query_string=message['query_string'].decode('utf-8'),
            headers=headers_dict,
            body=body,
            data=parsed_body,
            client=message['client'],
            server=message['server'],
        )
