from lemon.app import Lemon
from lemon.context import Context


async def handle(ctx: Context):
    data = ctx.req.data
    ctx.body = {
        'file_content': data['file'].read().decode(),
    }


app = Lemon(debug=True)

app.use(handle)

app.listen()
