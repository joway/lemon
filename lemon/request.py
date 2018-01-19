import json
from urllib.parse import parse_qs

from lemon.const import MIME_TYPES


class Request:
    """The Request object store the current request's fully information

    Example usage:
            ctx.req
    """

    def __init__(
            self, http_version, method, scheme,
            path, query_string, headers, body,
            client, server,
    ):
        self.http_version = http_version
        self.method = method.upper()
        self.scheme = scheme
        self.path = path
        self.query_string = query_string
        self.body = body
        self.client = client
        self.server = server

        # for cache
        self._headers = headers
        self._headers_dict = None
        self._json = None
        self._query = None

    @property
    def headers(self):
        if self._headers_dict:
            return self._headers_dict
        _headers_dict = {}
        for h in self._headers:
            _headers_dict[h[0].decode()] = h[1].decode()
        self._headers_dict = _headers_dict
        return self._headers_dict

    @property
    def protocol(self):
        """http or https
        """
        return self.scheme

    @property
    def secure(self):
        """is using https protocol
        """
        return self.scheme == 'https'

    @property
    def host(self):
        """HTTP_HEADERS['Host']
        """
        return self.headers.get('host', '')

    @property
    def content_type(self):
        """
        :return: dict
        """
        return self.headers.get('content-type', MIME_TYPES.TEXT_PLAIN)

    @property
    def query(self):
        if self._query is None:
            _q = parse_qs(self.query_string)
            self._query = {k: _q[k][0] for k in _q}
        return self._query

    @property
    def json(self):
        """Transform request body to dict when content_type is 'application/json'
        :return: dict
        """
        if self._json:
            return self._json
        self._json = json.loads(
            self.body if isinstance(self.body, str) else self.body.decode()
        )
        return self._json

    @classmethod
    async def read_body(cls, message, channels):
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
    async def from_asgi_interface(cls, message, channels):
        body = await cls.read_body(message, channels)
        return Request(
            http_version=message['http_version'],
            method=message['method'],
            scheme=message['scheme'],
            path=message['path'],
            query_string=message['query_string'].decode('utf-8'),
            headers=message['headers'],
            body=body,
            client=message['client'],
            server=message['server'],
        )
