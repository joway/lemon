from lemon.config import settings
from tests.base import HttpBasicTest


class TestConfig(HttpBasicTest):
    def test_config(self):
        local_config = {
            'LEMON_SERVER_HOST': '1.2.3.4',
        }
        settings.set_config(local_config)
        assert settings['LEMON_SERVER_HOST'] == '1.2.3.4'
        assert settings.LEMON_SERVER_HOST == '1.2.3.4'
        assert settings['LEMON_ROUTER_SLASH_SENSITIVE'] is False
        assert settings.LEMON_ROUTER_SLASH_SENSITIVE is False
