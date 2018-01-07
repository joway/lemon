from lemon.app import Lemon
from lemon.context import Context


async def middleware_exception(ctx: Context):
    raise Exception('error')


app = Lemon(debug=True)

app.use(middleware_exception)

app.listen()
