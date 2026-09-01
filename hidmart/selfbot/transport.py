class Transport:
    def __init__(self):
        self.connected = False

    async def connect(self):
        self.connected = True

    async def disconnect(self):
        self.connected = False

    async def request(self, method, payload=None):
        if not self.connected:
            raise RuntimeError("Transport is not connected")

        raise NotImplementedError(
            "A service-specific transport adapter is required."
        )