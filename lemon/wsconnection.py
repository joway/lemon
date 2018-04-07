class WSHeaders(dict):
    def __init__(self, raw_headers=None, *args, **kwargs):
        super(WSHeaders, self).__init__(*args, **kwargs)
        if raw_headers:
            for h in raw_headers:
                self.__setitem__(h[0].decode(), h[1].decode())

    def __setitem__(self, key: str, value):
        return super(WSHeaders, self).__setitem__(key.lower(), str(value))

    def __getitem__(self, key: str):
        return super(WSHeaders, self).__getitem__(key.lower())

    def set(self, key: str, value):
        return self.__setitem__(key, value)


class WSConnection:
    def __init__(self, conn):
        self.conn = conn

    async def establish(self):
        self.conn.accept()
        self.conn.listen()
        self.conn.connection_open()

    async def destroy(self):
        self.conn.reject()
        await self.conn.close()

    async def send(self, message_text: str):
        return await self.conn.send(message_text)


class WSMessage(dict):
    def __init__(self, raw_message, **kwargs):
        self.path = raw_message['path']
        self.order = raw_message['order']
        self.text = raw_message['text']
        self.bytes = raw_message['bytes']

        super().__init__(**kwargs)
