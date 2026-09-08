from __future__ import annotations

from ..transport.grpc_web import (
    encode,
    decode,
)


class RPCClient:

    def __init__(self, transport):

        self.transport = transport

    async def call(
        self,
        payload: bytes,
    ):

        frame = encode(payload)

        await self.transport.send(
            frame
        )

        data = (
            await self.transport.receive()
        )

        frames = decode(data)

        for trailer, body in frames:

            if not trailer:
                return body

        raise RuntimeError(
            "RPC response has no data frame"
        )