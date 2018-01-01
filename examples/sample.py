from random import random

from lemon.app import Lemon
from lemon.context import Context


async def middleware(ctx: Context, nxt):
    ctx.body = {
        'msg': 'hello world'
    }
    await nxt()


async def handle(ctx: Context):
    ctx.body['ack'] = 'yeah !'
    ctx.body['random'] = random()


app = Lemon(debug=True)

app.use(middleware)

app.use(handle)

app.listen()
