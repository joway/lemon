from lemon.app import Lemon
from lemon.context import Context


async def handle(ctx: Context):
    my_cookie = ctx.req.cookies.get('my_cookie')
    ctx.body = {
        'my_cookie': my_cookie,
    }


app = Lemon(debug=True)

app.use(handle)

app.listen()
