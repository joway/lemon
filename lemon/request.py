class Request:
    """The Request object store the current request's fully information

    Example usage:
            ctx.req
    """

    def __init__(
            self, http_version, method, scheme,
            path, query_string, headers, body,
            client, server,
    ):
        self.http_version = http_version
        self.method = method.upper()
        self.scheme = scheme
        self.path = path
        self.query_string = query_string
        self.headers = headers
        self.body = body
        self.client = client
        self.server = server

    @classmethod
    async def read_body(cls, message, channels):
        """
        Read and return the entire body from an incoming ASGI message.
        """
        body = message.get('body', b'')
        if 'body' in channels:
            while True:
                message_chunk = await channels['body'].receive()
                body += message_chunk['content']
                if not message_chunk.get('more_content', False):
                    break
        return body

    @classmethod
    async def from_asgi_interface(cls, message, channels):
        body = await cls.read_body(message, channels)
        return Request(
            http_version=message['http_version'],
            method=message['method'],
            scheme=message['scheme'],
            path=message['path'],
            query_string=message['query_string'],
            headers=message['headers'],
            body=body,
            client=message['client'],
            server=message['server'],
        )
