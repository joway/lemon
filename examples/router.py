from lemon.app import Lemon
from lemon.context import Context
from lemon.router import SimpleRouter


async def middleware(ctx: Context, nxt):
    ctx.body = {
        'msg': 'hello lemon'
    }
    await nxt()


async def handler1(ctx: Context):
    ctx.body['ack'] = 'yeah !'


async def handler2(ctx: Context):
    ctx.body['ack'] = 'yeah !'
    ctx.body['data'] = ctx.req.json


app = Lemon(debug=True)

router = SimpleRouter()
router.get('/handler1', middleware, handler1)
router.post('/handler2', middleware, handler2)

app.use(router.routes())

app.listen()
