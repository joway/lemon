from lemon.app import Lemon
from lemon.context import Context


async def middleware(ctx: Context, nxt):
    ctx.body = {
        'msg': 'hello world'
    }


async def handle(ctx: Context):
    ctx.body['ack'] = 'yeah !'


app = Lemon()

app.use(middleware)

app.use(handle)

app.listen()
