from lemon.app import Lemon
from lemon.context import Context


async def handle(ctx: Context):
    raise Exception('error')


app = Lemon(debug=True)

app.use(handle)

app.listen()
