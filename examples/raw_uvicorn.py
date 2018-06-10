import uvicorn


class EchoBody():
    def __init__(self, scope):
        self.scope = scope

    async def read_body(self, receive):
        """
        Read and return the entire body from an incoming ASGI message.
        """
        body = b''
        more_body = True

        while more_body:
            message = await receive()
            body += message.get('body', b'')
            more_body = message.get('more_body', False)

        return body

    async def __call__(self, receive, send):
        body = await self.read_body(receive)
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/plain'],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': body,
        })


uvicorn.run(EchoBody, host='127.0.0.1', port='9998')
