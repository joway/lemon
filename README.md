# Lemon

Lemon is an async and lightweight restful framework for python .  Inspired by koa .

## Usage

```python

async def middleware(ctx: Context, nxt):
    ctx.body = {
        'msg': 'hello world'
    }


async def handle(ctx: Context):
    ctx.body['ack'] = 'yeah !'


app = Lemon()

app.use(middleware)
app.use(handle)

app.listen(port=9999)

```
