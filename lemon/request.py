from httptools import parse_url


class Request(dict):
    def __init__(self, url_bytes, headers, version, method, transport, **kwargs):
        super().__init__(**kwargs)

        self._body = []
        self.body = None

        self.url = parse_url(url_bytes)
        self.headers = headers
        self.version = version
        self.method = method
        self.transport = transport

    def recv_body(self, body: bytes):
        self._body.append(body)

    def fin_body(self):
        self.body = b''.join(self._body)
