import typing
from abc import ABCMeta, abstractmethod

import kua

from lemon.app import exec_middleware
from lemon.config import settings
from lemon.const import HTTP_METHODS
from lemon.exception import LemonRouterRegisterError, RequestNotFoundError

_HTTP_METHODS = [
    HTTP_METHODS.GET,
    HTTP_METHODS.PUT,
    HTTP_METHODS.POST,
    HTTP_METHODS.DELETE,
    HTTP_METHODS.OPTIONS,
]


def _clean_slash(path: str):
    if path and path[-1] == '/':
        path = path[:-1]
    return path


class AbstractRouter(metaclass=ABCMeta):
    @abstractmethod
    def use(self, methods: list, path: str, *middleware_list) -> None:
        """Register routes
        :param methods: GET|PUT|POST|DELETE
        :param path: string
        :param middleware_list: async function(ctx, [nxt]) list
        """
        raise NotImplementedError

    @abstractmethod
    def routes(self) -> typing.Callable:
        """Return async function(ctx, [nxt])
        """
        raise NotImplementedError

    @abstractmethod
    def match(self, ctx) -> typing.List:
        """Return route
        """
        raise NotImplementedError


class AbstractBaseRouter(AbstractRouter, metaclass=ABCMeta):
    def get(self, path: str, *middleware_list) -> None:
        """Register GET routes
        :param path: url path
        :param middleware_list: async function(ctx, [nxt]) list
        """
        return self.use([HTTP_METHODS.GET], path, *middleware_list)

    def put(self, path: str, *middleware_list) -> None:
        """Register PUT routes
        :param path: url path
        :param middleware_list: async function(ctx, [nxt]) list
        """
        return self.use([HTTP_METHODS.PUT], path, *middleware_list)

    def post(self, path: str, *middleware_list) -> None:
        """Register POST routes
        :param path: url path
        :param middleware_list: async function(ctx, [nxt]) list
        """
        return self.use([HTTP_METHODS.POST], path, *middleware_list)

    def delete(self, path: str, *middleware_list) -> None:
        """Register DELETE routes
        :param path: url path
        :param middleware_list: async function(ctx, [nxt]) list
        """
        return self.use([HTTP_METHODS.DELETE], path, *middleware_list)

    def all(self, path: str, *middleware_list) -> None:
        """Register routes into all http methods
        :param path: url path
        :param middleware_list: async function(ctx, [nxt]) list
        """
        return self.use([
            HTTP_METHODS.GET,
            HTTP_METHODS.PUT,
            HTTP_METHODS.POST,
            HTTP_METHODS.DELETE,
        ], path, *middleware_list)

    def routes(self) -> typing.Callable:
        """Generate async router function(ctx, nxt)
        """

        async def _routes(ctx, nxt=None) -> None:
            method = ctx.req.method
            path = ctx.req.path
            middleware_list = self.match(ctx=ctx)

            if len(middleware_list) == 0:
                raise RequestNotFoundError

            await exec_middleware(ctx, middleware_list)

            if nxt:
                await nxt()

        return _routes


class SimpleRouter(AbstractBaseRouter, metaclass=ABCMeta):
    def __init__(self, slash=settings.LEMON_ROUTER_SLASH_SENSITIVE) -> None:
        self.slash = slash
        self._routes: dict = {
            HTTP_METHODS.GET: {},
            HTTP_METHODS.PUT: {},
            HTTP_METHODS.POST: {},
            HTTP_METHODS.DELETE: {},
        }

    def match(self, ctx) -> typing.List:
        method = ctx.req.method
        path = ctx.req.path

        if not self.slash:
            path = _clean_slash(path)

        if path not in self._routes[method]:
            raise RequestNotFoundError

        return self._routes[method][path]

    def use(self, methods: list, path: str, *middleware_list) -> None:
        """Register routes
        :param methods: GET|PUT|POST|DELETE
        :param path: string
        :param middleware_list: async function(ctx, [nxt]) list
        """
        for method in methods:
            if method not in _HTTP_METHODS:
                raise LemonRouterRegisterError
            if not self.slash:
                path = _clean_slash(path)
            self._routes[method][path] = list(middleware_list)


class Router(AbstractBaseRouter):
    def __init__(self, slash=settings.LEMON_ROUTER_SLASH_SENSITIVE) -> None:
        self.slash = slash
        self._routes = {
            HTTP_METHODS.GET: kua.Routes(),
            HTTP_METHODS.PUT: kua.Routes(),
            HTTP_METHODS.POST: kua.Routes(),
            HTTP_METHODS.DELETE: kua.Routes(),
        }

    def use(self, methods: list, path: str, *middleware_list) -> None:
        """Register routes
        :param methods: GET|PUT|POST|DELETE
        :param path: string
        :param middleware_list: async function(ctx, [nxt]) list
        """
        for method in methods:
            if method not in _HTTP_METHODS:
                raise LemonRouterRegisterError
            self._register_middleware_list(method, path, *middleware_list)

    def match(self, ctx) -> typing.Any:
        method = ctx.req.method
        path = ctx.req.path

        if not self.slash:
            path = _clean_slash(path)

        if method not in _HTTP_METHODS:
            raise RequestNotFoundError
        try:
            route = self._routes[method].match(path)
            ctx.params = route.params
            return route.anything
        except kua.RouteError:
            raise RequestNotFoundError

    def _register_middleware_list(
            self, method: str, path: str, *middleware_list
    ) -> None:
        if not self.slash:
            path = _clean_slash(path)

        if method not in _HTTP_METHODS:
            raise LemonRouterRegisterError

        return self._routes[method].add(path, list(middleware_list))
