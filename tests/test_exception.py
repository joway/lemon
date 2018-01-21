from lemon.exception import (
    MiddlewareParamsError,
    RouterRegisterError,
    RouterMatchError,
    RequestBodyParserError,
    GeneralException
)
from tests.base import BasicTest


class TestException(BasicTest):
    def test_exception(self):
        try:
            raise GeneralException(status=400, body='err')
        except GeneralException as e:
            assert e.status == 400
            assert e.body == 'err'

        try:
            raise MiddlewareParamsError
        except GeneralException as e:
            assert e.status == 500

        try:
            raise MiddlewareParamsError
        except MiddlewareParamsError as e:
            assert e.status == 500

        try:
            raise RouterRegisterError
        except RouterRegisterError as e:
            assert e.status == 500

        try:
            raise RouterMatchError
        except RouterMatchError as e:
            assert e.status == 500

        try:
            raise RequestBodyParserError
        except RequestBodyParserError as e:
            assert e.status == 400
