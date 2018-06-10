from lemon.config import settings
from lemon.exception import LemonConfigKeyError
from tests import BasicHttpTestCase


class TestConfig(BasicHttpTestCase):
    def test_config(self):
        local_config = {
            'LEMON_SERVER_HOST': '1.2.3.4',
        }
        settings.set_config(local_config)
        assert settings['LEMON_SERVER_HOST'] == '1.2.3.4'
        assert settings.LEMON_SERVER_HOST == '1.2.3.4'
        assert settings['LEMON_ROUTER_SLASH_SENSITIVE'] is False
        assert settings.LEMON_ROUTER_SLASH_SENSITIVE is False

        try:
            xxx = settings.XXX
            assert False
        except LemonConfigKeyError as e:
            pass
