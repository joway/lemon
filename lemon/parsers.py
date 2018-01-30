import json
import typing
from io import BytesIO

from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.formparser import FormDataParser
from werkzeug.http import parse_options_header
from werkzeug.urls import url_decode

import lemon.exception as exception
from lemon.const import MIME_TYPES


def get_mimetype_and_options(headers: dict) -> typing.Tuple[str, dict]:
    content_type = headers.get('content-type')
    if content_type:
        return parse_options_header(content_type)
    return '', {}


def get_content_length(headers: dict) -> typing.Optional[int]:
    if headers is None:
        raise exception.RequestHeadersParserError
    content_length = headers.get('content-length')
    if content_length is not None:
        try:
            return max(0, int(content_length))
        except (ValueError, TypeError):
            pass
    return None


def json_parser(body: bytes, *args) -> ImmutableMultiDict:
    if not body:
        raise exception.BadRequestError(body={
            'error': 'Empty Body',
        })
    try:
        return ImmutableMultiDict(json.loads(body.decode('utf-8')))
    except json.JSONDecodeError:
        raise exception.BadRequestError(body={
            'error': 'Invalid JSON',
        })


def url_encoded_parser(body: bytes, *args) -> dict:
    return url_decode(body, cls=ImmutableMultiDict)


def multi_part_parser(body: bytes, headers: dict = None) -> ImmutableMultiDict:
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
    for parser_mimetype in DEFAULT_PARSERS_MAPPING:
        if parser_mimetype == content_type:
            return DEFAULT_PARSERS_MAPPING[parser_mimetype](body, headers)
    return None
