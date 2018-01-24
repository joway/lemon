import typing

from lemon.exception import LemonConfigKeyError


class LemonConfig:
    def __init__(self, default_config: typing.Dict = None, config: typing.Dict = None):
        self._default_config = default_config or {}
        self._config = config or {}

    def set_config(self, config: typing.Dict):
        self._config = config or {}

    def __getattr__(self, key: typing.Text):
        if key.startswith('_'):
            return self.__getattribute__(key)
        return self.__getitem__(key)

    def __getitem__(self, key: typing.Text):
        try:
            return self._config[key]
        except KeyError:
            try:
                return self._default_config[key]
            except KeyError:
                raise LemonConfigKeyError


GLOBAL_CONFIG = {
    # SERVER
    'LEMON_SERVER_HOST': '127.0.0.1',
    'LEMON_SERVER_PORT': '9999',
    # CORS
    'LEMON_CORS_ENABLE': True,
    'LEMON_CORS_ORIGIN_ALLOW_ALL': False,
    'LEMON_CORS_ORIGIN_REGEX_WHITELIST': '',
    # ROUTER
    'LEMON_ROUTER_SLASH_SENSITIVE': False,
}

settings = LemonConfig(default_config=GLOBAL_CONFIG)
