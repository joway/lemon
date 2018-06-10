from lemon.app import Lemon
from lemon.context import Context


async def handle(ctx: Context):
    data = ctx.req.data
    file = data['file_content']
    ctx.body = {
        'file_content': file.read().decode(),
    }


app = Lemon(debug=True)

app.use(handle)

app.listen()
