import asyncio

import uvloop


def serve():
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(buy_potatos())
    loop.close()


if __name__ == '__main__':
    serve()
