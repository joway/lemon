class Context:
    def __init__(self):
        self.body = None

    def set(self, k, v):
        self.__setattr__(k, v)
