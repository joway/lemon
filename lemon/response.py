STATUS_CODES = {
    100: b'Continue',
    101: b'Switching Protocols',
    102: b'Processing',
    200: b'OK',
    201: b'Created',
    202: b'Accepted',
    203: b'Non-Authoritative Information',
    204: b'No Content',
    205: b'Reset Content',
    206: b'Partial Content',
    207: b'Multi-Status',
    208: b'Already Reported',
    226: b'IM Used',
    300: b'Multiple Choices',
    301: b'Moved Permanently',
    302: b'Found',
    303: b'See Other',
    304: b'Not Modified',
    305: b'Use Proxy',
    307: b'Temporary Redirect',
    308: b'Permanent Redirect',
    400: b'Bad Request',
    401: b'Unauthorized',
    402: b'Payment Required',
    403: b'Forbidden',
    404: b'Not Found',
    405: b'Method Not Allowed',
    406: b'Not Acceptable',
    407: b'Proxy Authentication Required',
    408: b'Request Timeout',
    409: b'Conflict',
    410: b'Gone',
    411: b'Length Required',
    412: b'Precondition Failed',
    413: b'Request Entity Too Large',
    414: b'Request-URI Too Long',
    415: b'Unsupported Media Type',
    416: b'Requested Range Not Satisfiable',
    417: b'Expectation Failed',
    418: b'I\'m a teapot',
    422: b'Unprocessable Entity',
    423: b'Locked',
    424: b'Failed Dependency',
    426: b'Upgrade Required',
    428: b'Precondition Required',
    429: b'Too Many Requests',
    431: b'Request Header Fields Too Large',
    451: b'Unavailable For Legal Reasons',
    500: b'Internal Server Error',
    501: b'Not Implemented',
    502: b'Bad Gateway',
    503: b'Service Unavailable',
    504: b'Gateway Timeout',
    505: b'HTTP Version Not Supported',
    506: b'Variant Also Negotiates',
    507: b'Insufficient Storage',
    508: b'Loop Detected',
    510: b'Not Extended',
    511: b'Network Authentication Required'
}


class Response:
    def __init__(
            self, body=None, status=200, headers=None,
            content_type='text/plain', body_bytes=b'',
    ):
        self.content_type = content_type
        self.body = body
        self.status = status
        self.headers = headers or {}

    @staticmethod
    def _encode_body(data):
        try:
            return data.encode()
        except AttributeError:
            return str(data).encode()

    def _parse_headers(self):
        headers = b''
        for name, value in self.headers.items():
            try:
                headers += \
                    (b'%b: %b\r\n' % (name.encode(), value.encode('utf-8')))
            except AttributeError:
                headers += \
                    (b'%b: %b\r\n' % (str(name).encode(), str(value).encode('utf-8')))

        return headers

    def output(
            self, version="1.1", keep_alive=False, keep_alive_timeout=None):
        body_bytes = self._encode_body(self.body)

        # This is all returned in a kind-of funky way
        # We tried to make this as fast as possible in pure python
        timeout_header = b''
        if keep_alive and keep_alive_timeout is not None:
            timeout_header = b'Keep-Alive: %d\r\n' % keep_alive_timeout
        self.headers['Content-Length'] = self.headers.get(
            'Content-Length', len(body_bytes))
        self.headers['Content-Type'] = self.headers.get(
            'Content-Type', self.content_type)

        headers = self._parse_headers()

        if self.status is 200:
            status = b'OK'
        else:
            status = STATUS_CODES.get(self.status, b'UNKNOWN RESPONSE')

        return (
                   b'HTTP/%b %d %b\r\n'
                   b'Connection: %b\r\n'
                   b'%b'
                   b'%b\r\n'
                   b'%b') % \
               (
                   version.encode(),
                   self.status,
                   status,
                   b'keep-alive' if keep_alive else b'close',
                   timeout_header,
                   headers,
                   body_bytes
               )
