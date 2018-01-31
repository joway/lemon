<p align="center"><a href="https://lemon.joway.io" target="_blank"><img width="100%" src="docs/images/lemon-long.png" alt="Lemon logo"></a></p>

<p align="center">
	<a target="_blank" href="https://travis-ci.org/joway/lemon"><img src="https://travis-ci.org/joway/lemon.svg?branch=master" alt="Build Status"></a>
   <a target="_blank" href="https://coveralls.io/github/joway/lemon?branch=master"><img src="https://coveralls.io/repos/github/joway/lemon/badge.svg?branch=master" alt="Coverage Status"></a>
   <a target="_blank" href="https://www.codacy.com/app/joway/lemon?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=joway/lemon&amp;utm_campaign=Badge_Grade"><img src="https://api.codacy.com/project/badge/Grade/f7f2ffd3c5f74732bb445e4cde9216a8" alt="Codacy Badge"></a>
</p>
<p align="center">
	<a target="_blank" href="https://pypi.python.org/pypi/pylemon"><img src="https://img.shields.io/pypi/v/pylemon.svg" alt="PyPi Version"></a>
	<a target="_blank" href="https://pypi.python.org/pypi/pylemon"><img src="https://img.shields.io/pypi/pyversions/pylemon.svg" alt="Python Version"></a>
   <a target="_blank" href="https://pypi.python.org/pypi/pylemon"><img src="https://img.shields.io/pypi/status/pylemon.svg" alt="PyPI"></a>
   <a target="_blank" href="https://github.com/joway/lemon/blob/master/LICENSE"><img src="https://img.shields.io/github/license/joway/lemon.svg" alt="license"></a>
   <a target="_blank" href="https://app.fossa.io/projects/git%2Bgithub.com%2Fjoway%2Flemon?ref=badge_shield"><img src="https://app.fossa.io/api/projects/git%2Bgithub.com%2Fjoway%2Flemon.svg?type=shield" alt="FOSSA Status"></a>
</p>

<h5 align="center">Lemon is an async and lightweight API framework for python .  Inspired by <a src="https://github.com/koajs/koa" target="_blank">Koa</a> and <a src="https://github.com/channelcat/sanic" target="_blank"> Sanic </a> .</h5>

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
- [x] add typing
- [x] lemon ctx.req.form
- [x] cookies
- [x] cors_middleware
- [ ] documentation
- [ ] benchmark
- [ ] websocket
