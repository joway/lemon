from random import random

from lemon.app import Lemon
from lemon.context import Context
from lemon.router import Router


async def middleware(ctx: Context, nxt):
    ctx.body = {
        'msg': 'hello lemon'
    }
    await nxt()


async def handler1(ctx: Context):
    ctx.body['ack'] = 'yeah !'
    ctx.body['random'] = random()


async def handler2(ctx: Context):
    for f in ctx.req.form:
        print(f.headers)
        print(f.text)
    ctx.body['ack'] = 'yeah !'
    ctx.body['random'] = random()


app = Lemon(debug=True)

router = Router()
router.get('/handler1', middleware, handler1)
router.post('/handler2', middleware, handler2)

app.use(router.routes())

app.listen()
