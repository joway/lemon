# Lemon 🍋

[![Build Status](https://travis-ci.org/joway/lemon.svg?branch=master)](https://travis-ci.org/joway/lemon)
[![Coverage Status](https://coveralls.io/repos/github/joway/lemon/badge.svg?branch=master)](https://coveralls.io/github/joway/lemon?branch=master)
[![Documentation Status](https://readthedocs.org/projects/pylemon/badge/?version=latest)](http://pylemon.readthedocs.io/en/latest/?badge=latest)
[![PyPi Version](https://img.shields.io/pypi/v/pylemon.svg)](https://pypi.python.org/pypi/pylemon)
[![Python Version](https://img.shields.io/pypi/pyversions/pylemon.svg)](https://pypi.python.org/pypi/pylemon)
[![PyPI](https://img.shields.io/pypi/status/pylemon.svg)](https://pypi.python.org/pypi/pylemon)
[![license](https://img.shields.io/github/license/joway/lemon.svg)](https://github.com/joway/lemon/blob/master/LICENSE)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fjoway%2Flemon.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fjoway%2Flemon?ref=badge_shield)

Lemon is an async and lightweight API framework for python .  Inspired by [Koa](https://github.com/koajs/koa) and [Sanic](https://github.com/channelcat/sanic) .


## Status

ALPHA

## Documentation

[https://lemon.joway.io](https://lemon.joway.io/#/)

## Installation

```shell
pip install -U pylemon
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

app.use(middleware, handler)

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
    ctx.body = ctx.req.json


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
- [ ] lemon ctx.req.form
- [ ] documentation
- [ ] cookies
- [ ] cors
- [ ] benchmark
- [ ] https
