import json
import socket
from cgi import parse_header
from urllib.parse import urlunparse, parse_qs

from httptools import parse_url
from requests_toolbelt import MultipartDecoder

from lemon.config import LEMON_SERVER_KEEP_ALIVE_TIMEOUT
from lemon.const import MIME_TYPES
from lemon.exception import RequestParserError


# class RequestBodyForm:
#     """Form object for request body when content type
#     is 'application/x-www-form-urlencoded' or 'multipart/form-data'
#     """
#
#     def __init__(self):
#         pass

class Request(dict):
    """The Request object store the current request's fully information

    Example usage:
            ctx.req
    """

    def __init__(
            self, url_bytes, headers, version,
            method, transport, keep_alive=None,
            keep_alive_timeout=None, **kwargs
    ):
        super().__init__(**kwargs)

        self.body = None
        self._body = []
        self._json = None
        self._form = None
        self._parsed_url = parse_url(url_bytes)

        self.headers = headers
        self.version = version
        self.method = method.upper()
        self.transport = transport

        self.keep_alive = \
            keep_alive or \
            self.headers.get('connection', 'close') == 'keep-alive'
        self.keep_alive_timeout = \
            keep_alive_timeout or LEMON_SERVER_KEEP_ALIVE_TIMEOUT

    @property
    def protocol(self):
        """http or https
        """
        protocol = 'http'
        if self.transport.get_extra_info('sslcontext'):
            protocol += 's'
        return protocol

    @property
    def secure(self):
        """is using https protocol
        """
        return self.protocol == 'https'

    @property
    def host(self):
        """HTTP_HEADERS['Host']
        """
        return self.headers.get('Host', '')

    @property
    def path(self):
        """path of the request
        """
        return self._parsed_url.path.decode('utf-8')

    @property
    def json(self):
        """Transform request body to dict when content_type is 'application/json'
        :return: dict
        """
        if self._json:
            return self._json
        self._json = json.loads(self.body)
        return self._json

    @property
    def form(self):
        """Transform request body to a dict when content_type
        is 'application/x-www-form-urlencoded' and 'multipart/form-data'
        """
        if self._form:
            return self._form
        content_type, parameters = parse_header(self.type)
        if content_type == MIME_TYPES.APPLICATION_X_WWW_FORM_URLENCODED:
            kv_pairs = parse_qs(self.body.decode('utf-8'))
            self._form = {p[0]: p[1] for p in kv_pairs}
        elif content_type == MIME_TYPES.MULTIPART_FORM_DATA:
            # TODO: unify form data structure
            self._form = MultipartDecoder(self.body, self.type, 'utf-8').parts
        else:
            raise RequestParserError
        return self._form

    @property
    def querystring(self):
        if self._parsed_url.query:
            return self._parsed_url.query.decode('utf-8')
        else:
            return ''

    @property
    def query(self):
        """
        :return: dict
        """
        try:
            return json.loads(self.querystring)
        except json.JSONDecoder:
            return {}

    @property
    def search(self):
        """
        :return: ?k=v&...
        """
        return '?' + self.querystring

    @property
    def type(self):
        """
        :return: dict
        """
        return self.headers.get('content-type', 'text/plain')

    @property
    def url(self):
        """
        :return: eg: https://example.com/path/to?k=v
        """
        return urlunparse((
            self.protocol,
            self.host,
            self.path,
            None,
            self.querystring,
            None))

    @property
    def ip(self):
        """
        :return: xxx.xxx.xxx.xxx
        """

        if not hasattr(self, '_socket'):
            self._get_address()
        return self._ip

    def _get_address(self):
        sock = self.transport.get_extra_info('socket')

        if sock.family == socket.AF_INET:
            self._socket = (self.transport.get_extra_info('peername') or
                            (None, None))
            self._ip, self._port = self._socket
        elif sock.family == socket.AF_INET6:
            self._socket = (self.transport.get_extra_info('peername') or
                            (None, None, None, None))
            self._ip, self._port, *_ = self._socket
        else:
            self._ip, self._port = (None, None)

    def recv_body(self, body: bytes):
        self._body.append(body)

    def fin_body(self):
        self.body = b''.join(self._body)
