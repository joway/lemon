# Lemon 🍋


Lemon is an async and lightweight API framework for python .  Inspired by [Koa](https://github.com/koajs/koa) and [Sanic](https://github.com/channelcat/sanic) .

## Design

### Server

Use [Uvicorn](https://github.com/encode/uvicorn) as its backend server .

Uvicorn is a lightning-fast asyncio server using uvloop and httptools .

### Router

#### Class : Router

For `/api/:var/foo/:var2`

#### Class : SimpleRouter

For simple api rules : `/api/resourse/action`

### Context

`ctx`

### Request

Bind on `ctx.req` .

### Response

Bind on `ctx.res`


