import json

from lemon.const import MIME_TYPES
from lemon.exception import ResponseFormatError
from lemon.request import HttpHeaders


class Response:
    def __init__(
            self, status: int = 200, headers: HttpHeaders = None,
            body: str = None, content_type: str = MIME_TYPES.TEXT_PLAIN,
    ) -> None:
        self.status = status
        self.headers = headers if headers else HttpHeaders()
        self.content_type = content_type
        self.body = body or ''

    @property
    def message(self) -> dict:
        content = b''
        if isinstance(self.body, dict):
            self.content_type = MIME_TYPES.APPLICATION_JSON
            content = json.dumps(self.body).encode()
        elif isinstance(self.body, str):
            content = self.body.encode()
        elif isinstance(self.body, bytes):
            content = self.body
        else:
            raise ResponseFormatError

        header_pairs = [
            [b'content-type', self.content_type.encode()],
        ]
        for h in self.headers:
            header_pairs.append([
                h.encode(),
                self.headers[h].encode(),
            ])
        return {
            'status': self.status,
            'headers': header_pairs,
            'content': content,
        }
