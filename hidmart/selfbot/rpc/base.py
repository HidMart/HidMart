class RPCClient:

    def __init__(self, transport):
        self.transport = transport

    async def send(self, payload):
        await self.transport.send(payload)

    async def receive(self):
        return await self.transport.receive()