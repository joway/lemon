from abc import ABCMeta, abstractmethod
from inspect import signature

from treelib import Tree

from lemon.config import LEMON_ROUTER_SLASH_SENSITIVE
from lemon.exception import RouterRegisterError, RouterMatchError


class HTTP_METHODS:
    GET = 'GET'
    PUT = 'PUT'
    POST = 'POST'
    DELETE = 'DELETE'


_HTTP_METHODS = [
    HTTP_METHODS.GET,
    HTTP_METHODS.PUT,
    HTTP_METHODS.POST,
    HTTP_METHODS.DELETE,
]


class Route:
    def __init__(self, path, handlers):
        self.path = path
        self.handlers = handlers


class RouteTree:
    def __init__(self, leaves=None, handlers=None):
        self._tree = Tree()
        self.root = self._tree.create_node(tag='', identifier='/')

    def add(self, path: str, *handlers):
        """Register path with its handlers
        :param path:
        :param handlers:
        """
        segments = path.split('/')

        if len(segments) == 0:
            raise RouterRegisterError('Valid path : {0}'.format(path))

        parent_idf = None
        last_node = None
        for seg in segments:
            sep = '' if parent_idf == '/' else '/'
            idf = '{0}{1}{2}'.format(parent_idf or '', sep, seg)
            last_node = self._tree.get_node(idf)
            if not last_node:
                last_node = self._tree.create_node(
                    tag=seg,
                    identifier=idf,
                    parent=parent_idf,
                )
            parent_idf = idf
        last_node.data = Route(path, handlers)

        return last_node

    def match(self, path: str):
        """Match path
        :param path:
        :return: Route object
        """
        # accurate hit
        leaf = self._tree.get_node(path)
        if leaf:
            return leaf.data

        segments = path.split('/')[1:]
        parent_idf = self.root.identifier
        matched_node = None
        for i, seg in enumerate(segments):
            nodes = self._tree.children(parent_idf)
            _node = None
            for node in nodes:
                if seg == node.tag:
                    _node = node
                    break
                if node.tag[0] == ':':
                    _node = node
            if not _node:
                return None
            parent_idf = _node.identifier
            if i == len(segments) - 1:
                matched_node = _node

        if not matched_node:
            return None

        return matched_node.data


class AbstractRouter(metaclass=ABCMeta):
    @abstractmethod
    def use(self, methods: list, path: str, *handlers):
        """Register routes
        :param methods: GET|PUT|POST|DELETE
        :param path: string
        :param handlers: async function(ctx, [nxt]) list
        """
        raise NotImplementedError

    @abstractmethod
    def routes(self):
        """Return async function(ctx, [nxt])
        """
        raise NotImplementedError


class AbstractBaseRouter(AbstractRouter, metaclass=ABCMeta):
    def get(self, path: str, *handlers):
        """Register GET routes
        :param path: url path
        :param handlers: async function(ctx, [nxt]) list
        """
        return self.use([HTTP_METHODS.GET], path, *handlers)

    def put(self, path: str, *handlers):
        """Register PUT routes
        :param path: url path
        :param handlers: async function(ctx, [nxt]) list
        """
        return self.use([HTTP_METHODS.PUT], path, *handlers)

    def post(self, path: str, *handlers):
        """Register POST routes
        :param path: url path
        :param handlers: async function(ctx, [nxt]) list
        """
        return self.use([HTTP_METHODS.POST], path, *handlers)

    def delete(self, path: str, *handlers):
        """Register DELETE routes
        :param path: url path
        :param handlers: async function(ctx, [nxt]) list
        """
        return self.use([HTTP_METHODS.DELETE], path, *handlers)

    def all(self, path: str, *handlers):
        """Register routes into all http methods
        :param path: url path
        :param handlers: async function(ctx, [nxt]) list
        """
        return self.use([
            HTTP_METHODS.GET,
            HTTP_METHODS.PUT,
            HTTP_METHODS.POST,
            HTTP_METHODS.DELETE,
        ], path, *handlers)


class SimpleRouter(AbstractBaseRouter):
    def __init__(self, slash=LEMON_ROUTER_SLASH_SENSITIVE):
        self.slash = slash
        self._routes = {
            HTTP_METHODS.GET: {},
            HTTP_METHODS.PUT: {},
            HTTP_METHODS.POST: {},
            HTTP_METHODS.DELETE: {},
        }

    def use(self, methods: list, path: str, *handlers):
        """Register routes
        :param methods: GET|PUT|POST|DELETE
        :param path: string
        :param handlers: async function(ctx, [nxt]) list
        """
        for method in methods:
            if method not in _HTTP_METHODS:
                raise RouterRegisterError(
                    'Cannot support method : {0}'.format(method)
                )
            if not self.slash and path[-1] == '/':
                path = path[:-1]
            self._routes[method][path] = handlers

    def routes(self):
        """Generate async router function(ctx, nxt)
        """

        async def _routes(ctx, nxt):
            method = ctx.req.method
            path = ctx.req.path

            if not self.slash and path[-1] == '/':
                path = path[:-1]

            if path not in self._routes[method]:
                ctx.status = 404
                ctx.body = {
                    'lemon': 'NOT FOUND'
                }
                return

            _handlers = self._routes[method][path]
            for _handler in _handlers:
                _handler_params = signature(_handler).parameters
                if len(_handler_params) == 1:
                    await _handler(ctx)
                else:
                    await _handler(ctx, nxt)

        return _routes


class Router(AbstractBaseRouter):
    def __init__(self, slash=LEMON_ROUTER_SLASH_SENSITIVE):
        self.slash = slash
        self._routes = {
            HTTP_METHODS.GET: RouteTree(),
            HTTP_METHODS.PUT: RouteTree(),
            HTTP_METHODS.POST: RouteTree(),
            HTTP_METHODS.DELETE: RouteTree(),
        }

    def use(self, methods: list, path: str, *handlers):
        """Register routes
        :param methods: GET|PUT|POST|DELETE
        :param path: string
        :param handlers: async function(ctx, [nxt]) list
        """
        for method in methods:
            if method not in _HTTP_METHODS:
                raise RouterRegisterError(
                    'Cannot support method : {0}'.format(method)
                )
            self._register_handlers(method, path, *handlers)

    def routes(self):
        """Generate async router function(ctx, nxt)
        """

        async def _routes(ctx, nxt):
            method = ctx.req.method
            path = ctx.req.path
            route = self._match_handlers(method=method, path=path)

            if route is None:
                ctx.status = 404
                ctx.body = {
                    'lemon': 'NOT FOUND'
                }
                return

            for _handler in route.handlers:
                _handler_params = signature(_handler).parameters
                if len(_handler_params) == 1:
                    await _handler(ctx)
                else:
                    await _handler(ctx, nxt)

        return _routes

    def _register_handlers(self, method: str, path: str, *handlers):
        if not self.slash and path[-1] == '/':
            path = path[:-1]

        if method not in _HTTP_METHODS:
            raise RouterMatchError(
                'Method {0} is not supported'.format(method)
            )

        return self._routes[method].add(path, *handlers)

    def _match_handlers(self, method: str, path: str):
        if not self.slash and path[-1] == '/':
            path = path[:-1]

        if method not in _HTTP_METHODS:
            raise RouterMatchError(
                'Method {0} is not supported'.format(method)
            )

        return self._routes[method].match(path)
