# Lemon 🍋 [![Build Status](https://travis-ci.org/joway/lemon.svg?branch=master)](https://travis-ci.org/joway/lemon) [![Coverage Status](https://coveralls.io/repos/github/joway/lemon/badge.svg?branch=feature%2Ftestcase)](https://coveralls.io/github/joway/lemon?branch=feature%2Ftestcase)

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

## Hello Lemon Router

```
from random import random

from lemon.app import Lemon
from lemon.context import Context
from lemon.router import Router


async def middleware(ctx: Context, nxt):
    ctx.body = {
        'msg': 'hello lemon'
    }
    await nxt()


async def handler1(ctx: Context):
    ctx.body['ack'] = 'yeah !'
    ctx.body['random'] = random()


async def handler2(ctx: Context):
    ctx.body['ack'] = 'yeah !'
    ctx.body['random'] = random()


app = Lemon(debug=True)

router = Router()
router.get('/handler1', middleware, handler1)
router.post('/handler2', middleware, handler2)

app.use(router.routes())

app.listen()

```



## TODO

- [x] tests
- [x] lemon router
- [ ] wsgi
- [ ] documentation
- [ ] cookies
- [ ] cors
- [ ] https
- [ ] benchmark
