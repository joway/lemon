from lemon.app import Lemon
from lemon.context import Context


async def err_middleware(ctx: Context, nxt):
    ctx.body = {
        'msg': 'err_middleware'
    }
    try:
        await nxt()
    except Exception:
        ctx.body = {
            'msg': 'error handled'
        }


async def handle(ctx: Context):
    raise Exception('error')


app = Lemon(debug=True)

app.use(err_middleware)

app.use(handle)

app.listen()
