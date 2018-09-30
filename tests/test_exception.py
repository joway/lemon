from lemon.exception import (
    LemonMiddlewareParamsError,
    LemonRouterRegisterError,
    LemonRouterMatchError,
    RequestBodyParserError,
    GeneralException
)

from tests import BasicHttpTestCase


class TestException(BasicHttpTestCase):
    def test_exception(self):
        try:
            raise GeneralException(status=400, body='err')
        except GeneralException as e:
            assert e.status == 400
            assert e.body == 'err'

        try:
            raise LemonMiddlewareParamsError
        except GeneralException as e:
            assert e.status == 500

        try:
            raise LemonMiddlewareParamsError
        except LemonMiddlewareParamsError as e:
            assert e.status == 500

        try:
            raise LemonRouterRegisterError
        except LemonRouterRegisterError as e:
            assert e.status == 500

        try:
            raise LemonRouterMatchError
        except LemonRouterMatchError as e:
            assert e.status == 500

        try:
            raise RequestBodyParserError
        except RequestBodyParserError as e:
            assert e.status == 400
