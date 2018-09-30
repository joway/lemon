from lemon.exception import LemonConfigKeyError


class LemonConfig:
    def __init__(self, default_config: dict = None, config: dict = None) -> None:
        """
        :param default_config: default app config
        :param config: app config
        """
        self._default_config = default_config or {}
        self._config = config or {}

    def set_config(self, config: dict):
        """
        :param config: app config
        """
        self._config = config or {}

    def __getattr__(self, key: str):
        if key.startswith('_'):
            return self.__getattribute__(key)
        return self.__getitem__(key)

    def __getitem__(self, key: str):
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
    'LEMON_DEBUG': False,
    # ROUTER
    'LEMON_ROUTER_SLASH_SENSITIVE': False,
    # CORS
    'LEMON_CORS_ENABLE': False,
    'LEMON_CORS_ALLOW_METHODS': ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH'],
    'LEMON_CORS_ALLOW_HEADERS': [],
    'LEMON_CORS_EXPOSE_HEADERS': [],
    'LEMON_CORS_ALLOW_CREDENTIALS': False,
    'LEMON_CORS_ORIGIN_WHITELIST': [],
    'LEMON_CORS_ORIGIN_REGEX_WHITELIST': [],
    'LEMON_CORS_MAX_AGE': 86400,
}

settings = LemonConfig(default_config=GLOBAL_CONFIG)
