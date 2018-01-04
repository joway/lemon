from lemon.router import Router, SimpleRouter
from tests.base import HttpBasicTest


class TestRouter(HttpBasicTest):
    def test_sample_router(self):
        async def middleware(ctx, nxt):
            ctx.body = {'m': 'mid'}
            await nxt()

        async def handler1(ctx):
            ctx.body['app'] = 1

        async def handler2(ctx):
            ctx.body['app'] = 2

        router = SimpleRouter()
        router.get('/app/handler1', middleware, handler1)
        router.get('/app/handler2', middleware, handler2)

        client = self.create_http_server(handlers=[router.routes()])
        req = client.get('/app/handler1')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 1

        req = client.get('/app/handler2')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 2

        req = client.get('/app/handler2/')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 2

        req = client.get('/app/xxx/')
        data = req.json()
        assert req.status_code == 404
        assert data['lemon'] == 'NOT FOUND'

        client.stop_server()

    def test_router_example(self):
        async def middleware(ctx, nxt):
            ctx.body = {'m': 'mid'}
            await nxt()

        async def handler1(ctx):
            ctx.body['app'] = 1

        async def handler2(ctx):
            ctx.body['app'] = 2

        router = Router()
        router.get('/app/handler1', middleware, handler1)
        router.get('/app/handler2', middleware, handler2)

        client = self.create_http_server(handlers=[router.routes()])
        req = client.get('/app/handler1')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 1

        req = client.get('/app/handler2')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 2

        req = client.get('/app/handler2/')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 2

        req = client.get('/app/xxx/')
        data = req.json()
        assert req.status_code == 404
        assert data['lemon'] == 'NOT FOUND'

        client.stop_server()

    def test_router_register(self):
        async def middleware(ctx, nxt):
            ctx.body = {'m': 2}
            await nxt

        async def handler(ctx):
            ctx.body = {'x': 1}

        router = Router()
        router._register_handlers('GET', '/res/action', middleware, handler)

        route = router._match_handlers('GET', '/res')
        assert route is None

        route = router._match_handlers('GET', '/res/action/')
        assert route is not None
        assert route.path == '/res/action'
        assert len(route.handlers) == 2

        route = router._match_handlers('GET', '/res/action')
        assert route is not None
        assert route.path == '/res/action'
        assert len(route.handlers) == 2

    def test_rest_router_register(self):
        async def handler(ctx):
            ctx.body = {'x': 1}

        router = Router()
        router._register_handlers('GET', '/res/:id/action', handler)
        route = router._match_handlers('GET', '/res/xxx/action')
        assert route is not None
        assert route.path == '/res/:id/action'
        assert len(route.handlers) == 1

        route = router._match_handlers('GET', '/res/:id/action')
        assert route is not None
        assert route.path == '/res/:id/action'
        assert len(route.handlers) == 1

        route = router._match_handlers('GET', '/re/:id/action')
        assert route is None

        route = router._match_handlers('GET', '/res/:id/actions')
        assert route is None
