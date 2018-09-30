import pytest

from lemon.router import Router, SimpleRouter
from tests import BasicHttpTestCase


@pytest.mark.asyncio
class TestRouter(BasicHttpTestCase):
    async def test_full_router(self):
        async def single(ctx):
            ctx.body = {
                'app': 'single',
            }

        async def _all(ctx):
            ctx.body = {
                'app': 'all',
            }

        router = SimpleRouter()
        router.get('/app', single)
        router.put('/app', single)
        router.post('/app', single)
        router.delete('/app', single)

        router.all('/all', _all)
        self.app.use(router.routes())

        req = await self.get('/app')
        assert req.status_code == 200
        req = await self.put('/app')
        assert req.status_code == 200
        req = await self.post('/app')
        assert req.status_code == 200
        req = await self.delete('/app')
        assert req.status_code == 200

    async def test_sample_router(self):
        async def middleware(ctx, nxt):
            ctx.body = {'m': 'mid'}
            await nxt()

        async def handler1(ctx):
            ctx.body['app'] = 1

        async def handler2(ctx):
            ctx.body['app'] = 2

        router = SimpleRouter()
        router.get('/app/handler1', middleware, handler1)
        router.get('/app/handler1', middleware, handler1)
        router.get('/app/handler2', middleware, handler2)

        self.app.use(router.routes())
        req = await self.get('/app/handler1')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 1

        req = await self.get('/app/handler2')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 2

        req = await self.get('/app/handler2/')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 2

        req = await self.get('/app/xxx/')
        data = req.json()
        assert req.status_code == 404
        assert data['error'] == 'not found'

    async def test_router_example(self):
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

        self.app.use(router.routes())
        req = await self.get('/app/handler1')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 1

        req = await self.get('/app/handler2')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 2

        req = await self.get('/app/handler2/')
        data = req.json()
        assert req.status_code == 200
        assert data['m'] == 'mid'
        assert data['app'] == 2

        req = await self.get('/app/xxx/')
        data = req.json()
        assert req.status_code == 404
        assert data['error'] == 'not found'
    #
    # async def test_router_register(self):
    #     async def middleware(ctx, nxt):
    #         ctx.body = {'m': 2}
    #         await nxt
    #
    #     async def handler(ctx):
    #         ctx.body = {'x': 1}
    #
    #     router = Router()
    #     router._register_middleware_list(
    #         'GET', '/res/action', middleware, handler
    #     )
    #
    # async def test_rest_router_register(self):
    #     async def handler(ctx):
    #         ctx.body = {'x': 1}
    #
    #     router = Router()
    #     router._register_middleware_list('GET', '/res/:id/action', handler)
    #
    #     route = router._match_middleware_list('GET', '/res/xxx/action')
    #     assert route is not None
    #     assert route.params['id'] == 'xxx'
    #     assert len(route.anything) == 1
    #
    #     route = router._match_middleware_list('GET', '/res/:id/action')
    #     assert route is not None
    #     assert route.params['id'] == ':id'
    #     assert len(route.anything) == 1
    #
    #     route = router._match_middleware_list('GET', '/re/:id/action')
    #     assert route is None
    #
    #     route = router._match_middleware_list('GET', '/res/:id/actions')
    #     assert route is None

    async def test_router_exec(self):
        global before_count
        global after_count
        global handler_count
        global orders

        before_count = 0
        after_count = 0
        handler_count = 0
        orders = []

        async def before(ctx, nxt):
            ctx.body = {'count': 1}
            global before_count
            global orders
            orders.append(0)
            before_count += 1
            await nxt()

        async def handler1(ctx, nxt):
            ctx.body['count'] += 1
            global handler_count
            global orders
            orders.append(1)
            handler_count += 1
            await nxt()

        async def handler2(ctx, nxt):
            ctx.body['count'] += 1
            global handler_count
            global orders
            orders.append(2)
            handler_count += 1
            await nxt()

        async def handler3(ctx, nxt):
            ctx.body['count'] += 1
            global handler_count
            global orders
            orders.append(3)
            handler_count += 1
            await nxt()

        async def after(ctx):
            global after_count
            global orders
            orders.append(4)
            after_count += 1
            ctx.body['count'] += 1

        router = Router()
        router.get('/', handler1, handler2, handler3)

        self.app.use(before)
        self.app.use(router.routes())
        self.app.use(after)

        req = await self.get('/')
        data = req.json()
        assert req.status_code == 200
        assert data['count'] == 5
        assert before_count == 1
        assert after_count == 1
        assert handler_count == 3

        assert orders[0] == 0
        assert orders[1] == 1
        assert orders[2] == 2
        assert orders[3] == 3
        assert orders[4] == 4
