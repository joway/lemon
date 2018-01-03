import json
import socket
from cgi import parse_header
from urllib.parse import urlunparse, parse_qs

from httptools import parse_url
from requests_toolbelt import MultipartDecoder

from lemon.exception import RequestParserError


class Request(dict):

    def __init__(self, url_bytes, headers, version,
                 method, transport, **kwargs):
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

    @property
    def protocol(self):
        protocol = 'http'
        if self.transport.get_extra_info('sslcontext'):
            protocol += 's'
        return protocol

    @property
    def secure(self):
        return self.protocol == 'https'

    @property
    def host(self):
        return self.headers.get('Host', '')

    @property
    def path(self):
        return self._parsed_url.path.decode('utf-8')

    @property
    def json(self):
        if self._json:
            return self._json
        self._json = json.loads(self.body)
        return self._json

    @property
    def form(self):
        if self._form:
            return self._form
        content_type, parameters = parse_header(self.type)
        if content_type == 'application/x-www-form-urlencoded':
            kv_pairs = parse_qs(self.body.decode('utf-8'))
            self._form = {p[0]: p[1] for p in kv_pairs}
        elif content_type == 'multipart/form-data':
            # TODO: unify form data structure
            boundary = parameters['boundary'].encode('utf-8')
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
        try:
            return json.loads(self.querystring)
        except json.JSONDecoder:
            return {}

    @property
    def search(self):
        return '?' + self.querystring

    @property
    def type(self):
        return self.headers.get('content-type', 'text/plain')

    @property
    def url(self):
        return urlunparse((
            self.protocol,
            self.host,
            self.path,
            None,
            self.querystring,
            None))

    @property
    def ip(self):
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
