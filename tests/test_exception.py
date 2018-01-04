from lemon.exception import HandlerParamsError, RouterRegisterError, RouterMatchError, RequestParserError, HttpError
from tests.base import BasicTest


class TestException(BasicTest):
    def test_serve(self):
        try:
            raise HandlerParamsError
        except HandlerParamsError as e:
            assert e.msg == 'HandlerParamsError'

        try:
            raise RouterRegisterError
        except RouterRegisterError as e:
            assert e.msg == 'RouterRegisterError'

        try:
            raise RouterMatchError
        except RouterMatchError as e:
            assert e.msg == 'RouterMatchError'

        try:
            raise RequestParserError
        except RequestParserError as e:
            assert e.msg == 'RequestParserError'

        try:
            raise HttpError(status=400, body='err')
        except HttpError as e:
            assert e.status == 400
            assert e.body == 'err'
