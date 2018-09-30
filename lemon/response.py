import json

from lemon.const import MIME_TYPES, CHARSETS
from lemon.request import HttpHeaders


class Response:
    def __init__(
            self, status: int = 200, headers: HttpHeaders = None,
            body: str = None, content_type: str = MIME_TYPES.APPLICATION_JSON,
            charset: str = CHARSETS.UTF8,
    ) -> None:
        self.status = status
        self.headers = headers if headers else HttpHeaders()
        self.body = body or ''
        self.content_type = content_type
        self.charset = charset

    @property
    def raw_content_type(self):
        content_type = '{type}; {charset}'.format(
            type=self.content_type, charset=self.charset
        )
        return [b'content-type', content_type.encode()]

    @property
    def raw_headers(self):
        content_type_header = self.raw_content_type
        _raw_headers = self.headers.to_raw()
        _raw_headers.append(content_type_header)
        return _raw_headers

    @property
    def raw_body(self) -> bytes:
        _raw_body = b''
        if isinstance(self.body, dict):
            _raw_body = json.dumps(self.body).encode()
        elif isinstance(self.body, str):
            _raw_body = self.body.encode()
        elif isinstance(self.body, bytes):
            _raw_body = self.body
        return _raw_body
