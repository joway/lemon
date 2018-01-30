from lemon.app import Lemon
from lemon.context import Context


async def handle(ctx: Context):
    print(ctx.req.form.get('xxx'))
    ctx.body = {
        'get file': '',
    }


app = Lemon(debug=True)

app.use(handle)

app.listen()
