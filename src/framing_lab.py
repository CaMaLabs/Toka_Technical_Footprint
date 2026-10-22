"""Tiny, offline framing demonstration. This is not an implementation of any patent.

Synthetic record layout: 4-byte ASCII tag 'FRAM', 2-byte big-endian length,
followed by payload; records may be preceded by arbitrary noise bytes.
Never handles live devices or networks.
"""
from __future__ import annotations

MARKER = b"FRAM"
MAX_PAYLOAD = 65535


def frame(payload: bytes) -> bytes:
    if len(payload) > MAX_PAYLOAD:
        raise ValueError("payload too long")
    return MARKER + len(payload).to_bytes(2, "big") + payload


def recover(data: bytes) -> list[bytes]:
    """Extract complete synthetic records; reject truncated trailing records."""
    result = []
    cursor = 0
    while True:
        pos = data.find(MARKER, cursor)
        if pos == -1 or pos + 6 > len(data):
            break
        length = int.from_bytes(data[pos + 4:pos + 6], "big")
        end = pos + 6 + length
        if end > len(data):
            cursor = pos + 1
            continue
        result.append(data[pos + 6:end])
        cursor = end
    return result


def main() -> None:
    data = b"NOISE" + frame(b"synthetic-frame-1") + frame(b"synthetic-frame-2")
    print("Recovered synthetic payloads:", recover(data))


if __name__ == "__main__":
    main()
