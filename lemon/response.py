import json
import typing

from lemon.const import MIME_TYPES
from lemon.exception import ResponseFormatError


class Response:
    def __init__(
            self, status=200, headers: list = None,
            body=None, content_type=MIME_TYPES.TEXT_PLAIN,
    ) -> None:
        self.status = status
        self.headers = headers if headers else []
        self.content_type = content_type
        self.body = body or ''

    @property
    def message(self) -> typing.Dict:
        content = ''
        if isinstance(self.body, dict):
            self.content_type = MIME_TYPES.APPLICATION_JSON
            content = json.dumps(self.body).encode()
        elif isinstance(self.body, str):
            content = self.body.encode()
        elif isinstance(self.body, bytes):
            content = self.body
        else:
            raise ResponseFormatError

        self.headers.append([
            b'content-type',
            self.content_type.encode(),
        ])
        return {
            'status': self.status,
            'headers': self.headers,
            'content': content,
        }
