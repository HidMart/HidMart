from __future__ import annotations


class GRPCWebError(ValueError):
    pass


def encode(
    payload: bytes,
    trailer=False,
):

    if not isinstance(
        payload,
        bytes,
    ):
        payload = bytes(payload)

    flag = 0x80 if trailer else 0x00

    return (
        bytes([flag])
        + len(payload).to_bytes(
            4,
            "big",
        )
        + payload
    )


def decode(data: bytes):

    result = []

    offset = 0

    while offset < len(data):

        if len(data) - offset < 5:
            raise GRPCWebError(
                "incomplete frame"
            )

        flag = data[offset]

        size = int.from_bytes(
            data[
                offset + 1:
                offset + 5
            ],
            "big",
        )

        offset += 5

        if (
            len(data) - offset
            < size
        ):
            raise GRPCWebError(
                "incomplete payload"
            )

        payload = data[
            offset:
            offset + size
        ]

        offset += size

        result.append(
            (
                bool(flag & 0x80),
                payload,
            )
        )

    return result