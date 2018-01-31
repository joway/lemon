from lemon.app import Lemon
from lemon.context import Context


async def handle(ctx: Context):
    ctx.body = {
        'ok': True,
    }


app = Lemon(
    config={
        'LEMON_CORS_ENABLE': True,
    },
    debug=True,
)

app.use(handle)

app.listen()
