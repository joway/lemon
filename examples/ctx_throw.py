from lemon.app import Lemon
from lemon.context import Context


async def middleware(ctx: Context):
    ctx.throw(status=403, body={
        'msg': '403'
    })
    assert False


app = Lemon(debug=True)

app.use(middleware)

app.listen()
