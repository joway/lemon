# Lemon 🍋 [![Build Status](https://travis-ci.org/joway/lemon.svg?branch=master)](https://travis-ci.org/joway/lemon)

Lemon is an async and lightweight restful framework for python .  Inspired by [Koa](https://github.com/koajs/koa) and [Sanic](https://github.com/channelcat/sanic) .


## Status

ALPHA

## Installation

```shell
pip install pylemon
```

## Hello Lemon

```python
from lemon.app import Lemon
from lemon.context import Context

async def middleware(ctx: Context, nxt):
    ctx.body = {
        'msg': 'hello lemon'
    }
    await nxt()


async def handler(ctx: Context):
    ctx.body['ack'] = 'yeah !'

app = Lemon()

app.use(middleware)
app.use(handler)

app.listen(port=9999)

```

## TODO

- [ ] tests
- [ ] lemon router
- [ ] wsgi
- [ ] documentation
- [ ] cookies
- [ ] cors
- [ ] https
- [ ] benchmark
