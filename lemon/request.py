import typing
from urllib.parse import parse_qs

from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.http import parse_cookie

from lemon.const import MIME_TYPES


class HttpHeaders(dict):
    def __init__(self, raw_headers=None, *args, **kwargs):
        super(HttpHeaders, self).__init__(*args, **kwargs)
        if raw_headers:
            for h in raw_headers:
                self.__setitem__(h[0].decode(), h[1].decode())

    def __setitem__(self, key: str, value):
        return super(HttpHeaders, self).__setitem__(key.lower(), str(value))

    def __getitem__(self, key: str):
        return super(HttpHeaders, self).__getitem__(key.lower())

    def set(self, key: str, value):
        return self.__setitem__(key, value)

    def to_raw(self):
        raw_headers = []
        for k in self:
            raw_headers.append([
                k.encode(), self[k].encode(),
            ])
        return raw_headers


class Request:
    """The Request object store the current request's fully information

    Example usage:
            ctx.req
    """

    def __init__(
            self,
            http_version: str,
            method: str,
            scheme: str,
            path: str,
            query_string: bytes,
            headers: HttpHeaders,
            body: bytes,
            data: typing.Optional[ImmutableMultiDict],
            client: tuple,
            server: tuple,
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
        self._query: typing.Optional[dict] = None

    @property
    def protocol(self) -> str:
        """http or https
        """
        return self.scheme

    @property
    def secure(self) -> bool:
        """is using https protocol
        """
        return self.scheme == 'https'

    @property
    def host(self) -> str:
        """HTTP_HEADERS['Host']
        """
        return self.headers.get('host', '')

    @property
    def content_type(self) -> str:
        """HTTP_HEADERS['Content-Type']
        """
        return self.headers.get('content-type', MIME_TYPES.TEXT_PLAIN)

    @property
    def query(self) -> dict:
        if self._query is None:
            _q = parse_qs(self.query_string)
            self._query = {k: _q[k][0] for k in _q}
        return self._query

    @property
    def form(self) -> typing.Optional[ImmutableMultiDict]:
        return self.data

    @property
    def json(self) -> dict:
        """Transform request body to dict when content_type is 'application/json'
        :return: dict
        """
        return self.data.to_dict(flat=True) if self.data else None

    @property
    def cookies(self) -> dict:
        return parse_cookie(self.headers.get('cookie'))
