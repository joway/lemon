import json
import typing
from io import BytesIO

from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.formparser import FormDataParser
from werkzeug.http import parse_options_header
from werkzeug.urls import url_decode

from lemon.const import MIME_TYPES
from lemon.exception import RequestHeadersParserError, RequestBodyParserError


def get_mimetype_and_options(headers: dict) -> typing.Tuple[str, dict]:
    content_type = headers.get('content-type')
    if content_type:
        return typing.cast(typing.Tuple[str, dict], parse_options_header(content_type))
    return '', {}


def get_content_length(headers: dict) -> typing.Optional[int]:
    if headers is None:
        raise RequestHeadersParserError
    content_length = headers.get('content-length')
    if content_length is None:
        return None
    try:
        return max(0, int(content_length))
    except (ValueError, TypeError):
        raise RequestHeadersParserError


def json_parser(body: bytes, *args) -> ImmutableMultiDict:
    if not body:
        raise RequestBodyParserError
    try:
        return ImmutableMultiDict(json.loads(body.decode('utf-8')))
    except json.JSONDecodeError:
        raise RequestBodyParserError


def url_encoded_parser(body: bytes, *args) -> dict:
    return url_decode(body, cls=ImmutableMultiDict)


def multi_part_parser(body: bytes, headers: dict = {}) -> ImmutableMultiDict:
    mimetype, options = get_mimetype_and_options(headers)
    content_length = get_content_length(headers)
    parser = FormDataParser()
    _, form, files = parser.parse(
        BytesIO(body),
        mimetype,
        content_length,
        options
    )
    return ImmutableMultiDict(list(form.items()) + list(files.items()))


DEFAULT_PARSERS_MAPPING: typing.Dict[str, typing.Callable] = {
    MIME_TYPES.APPLICATION_JSON: json_parser,
    MIME_TYPES.APPLICATION_X_WWW_FORM_URLENCODED: url_encoded_parser,
    MIME_TYPES.MULTIPART_FORM_DATA: multi_part_parser,
}


def parse_http_body(headers: dict, body: bytes) -> typing.Optional[ImmutableMultiDict]:
    content_type, _ = get_mimetype_and_options(headers=headers)
    if content_type in DEFAULT_PARSERS_MAPPING:
        return DEFAULT_PARSERS_MAPPING[content_type](body, headers)
    return json_parser(body, headers)
