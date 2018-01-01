from lemon.app import Lemon
from lemon.context import Context


async def handle(ctx: Context):
    ctx.throw(status=403, body={
        'msg': '403'
    })
    assert False


app = Lemon(debug=True)

app.use(handle)

app.listen()
