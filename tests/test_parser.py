from lemon.exception import RequestHeadersParserError, BadRequestError
from lemon.parsers import get_content_length, json_parser, url_encoded_parser
from tests import BasicHttpTestCase


class TestParser(BasicHttpTestCase):
    def test_get_content_length(self):
        assert get_content_length({}) is None
        try:
            get_content_length({
                'content-length': 'xx',
            })
            assert False
        except RequestHeadersParserError:
            pass

        try:
            get_content_length(None)
        except RequestHeadersParserError:
            pass

    def test_json_parser(self):
        try:
            json_parser(None)
            assert False
        except BadRequestError:
            pass

        try:
            json_parser(b'{')
            assert False
        except BadRequestError:
            pass

    def test_url_encoded_parser(self):
        parsed = url_encoded_parser(b'title=test&sub%5B%5D=1&sub%5B%5D=2&sub%5B%5D=3')
        assert parsed['title'] == 'test'
