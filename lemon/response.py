import json

from lemon.const import HTTP_STATUS_CODE_MAPPING, MIME_TYPES


class Response:
    def __init__(
            self, body=None, status=200, headers=None,
            content_type=MIME_TYPES.TEXT_PLAIN,
            version='1.1', keep_alive=True, keep_alive_timeout=10,
    ):
        self.type = content_type
        self.body = body
        self.status = status
        self.headers = headers or {}
        self.http_version = version
        self.keep_alive = keep_alive
        self.keep_alive_timeout = keep_alive_timeout

    @property
    def message(self):
        """Status code message for human
        """
        return HTTP_STATUS_CODE_MAPPING.get(self.status, b'UNKNOWN RESPONSE')

    @property
    def body_bytes(self):
        """
        :return: bytes
        """
        return self._encode_body(self.body)

    @property
    def headers_bytes(self):
        """
        :return: bytes
        """
        _headers = b''
        for name, value in self.headers.items():
            try:
                _headers += \
                    (b'%b: %b\r\n' % (
                        name.encode(),
                        value.encode('utf-8')
                    ))
            except AttributeError:
                _headers += \
                    (b'%b: %b\r\n' % (
                        str(name).encode(),
                        str(value).encode('utf-8')
                    ))

        return _headers

    @property
    def length(self):
        """
        :return: length of response
        """
        return len(self.body_bytes)

    def datagram(self):
        """
        :param version:
        :param keep_alive:
        :param keep_alive_timeout:
        :return:
        """
        timeout_header = b''
        if self.keep_alive and self.keep_alive_timeout is not None:
            timeout_header = b'Keep-Alive: %d\r\n' % self.keep_alive_timeout

        self.headers['Content-Length'] = self.headers.get(
            'Content-Length', self.length,
        )
        self.headers['Content-Type'] = self.headers.get(
            'Content-Type', self.type,
        )

        return (
                   b'HTTP/%b %d %b\r\n'
                   b'Connection: %b\r\n'
                   b'%b'
                   b'%b\r\n'
                   b'%b'
               ) % (
                   self.http_version.encode(), self.status, self.message,
                   b'keep-alive' if self.keep_alive else b'close',
                   timeout_header,
                   self.headers_bytes,
                   self.body_bytes
               )

    def _encode_body(self, data):
        if isinstance(data, dict):
            self.type = MIME_TYPES.APPLICATION_JSON
            return json.dumps(data).encode()
        try:
            return data.encode()
        except AttributeError:
            return str(data).encode()
