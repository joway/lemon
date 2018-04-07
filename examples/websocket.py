import asyncio

from lemon.app import Lemon
from lemon.wsconnection import WSMessage, WSConnection

cache = []


async def pull(conn: WSConnection, msg: WSMessage):
    print(msg.text)
    await conn.send(msg.text)


async def push(conns):
    while True:
        for conn in conns:
            await conn.send('xxx')
        await asyncio.sleep(0.1)


ins = Lemon(debug=True)

ins.ws(ws_pull=pull, ws_push=push)

ins.listen()
