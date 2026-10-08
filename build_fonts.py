#!/usr/bin/env python3
"""Package pinned OFL fonts as WOFF with every source table preserved byte-for-byte.

No subsetting, renaming, metadata rewriting or glyph transformation is performed.
WOFF-specific metadata is omitted; all original metadata remains in its font tables.
Format: https://www.w3.org/TR/WOFF/
"""
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import quote
import hashlib
import struct
import zlib

ROOT = Path(__file__).resolve().parent
COMMIT = 'e9a263957eae262c5701d40b86eb1b2cbb9152e9'
SOURCES = [
    ('ofl/inter/Inter[opsz,wght].ttf', 'inter.woff', '29160a80ff49ddcab2c97711247e08b1fab27a484a329ce8b813d820dc559031'),
    ('ofl/manrope/Manrope[wght].ttf', 'manrope.woff', '3ae11c49db0455a3cc33e37d380f20fdb8c7f8b41dc07625c177e3d87a9d6ae6'),
    ('ofl/ibmplexmono/IBMPlexMono-Regular.ttf', 'ibm-plex-mono.woff', '6a3412f058c7d8dfd9170c41e85ade48e5156ecb89356110ca57a0a27734af46'),
]


def package(source):
    flavor, count = struct.unpack_from('>IH', source)
    records = []
    for i in range(count):
        tag, checksum, offset, length = struct.unpack_from('>4sIII', source, 12 + i * 16)
        records.append((tag, checksum, offset, source[offset:offset + length]))
    assert len({r[0] for r in records}) == count
    original = {tag: data for tag, _, _, data in records}
    assert b'name' in original and b'OS/2' in original
    cursor = 44 + count * 20
    entries, blocks = {}, []
    for tag, checksum, _, data in sorted(records, key=lambda r: r[2]):
        compressed = zlib.compress(data, 9)
        payload = compressed if len(compressed) < len(data) else data
        entries[tag] = struct.pack('>4sIIII', tag, cursor, len(payload), len(data), checksum)
        padded = payload + b'\0' * (-len(payload) % 4)
        blocks.append(padded)
        cursor += len(padded)
    revision = struct.unpack_from('>I', original[b'head'], 4)[0]
    sfnt_size = 12 + count * 16 + sum((len(data) + 3) & ~3 for data in original.values())
    header = struct.pack('>IIIHHIHHIIIII', 0x774F4646, flavor, cursor, count, 0,
                         sfnt_size, revision >> 16, revision & 0xFFFF, 0, 0, 0, 0, 0)
    result = header + b''.join(entries[tag] for tag in sorted(entries)) + b''.join(blocks)
    assert len(result) == cursor
    decoded = {}
    for i in range(count):
        tag, offset, compressed_length, length, checksum = struct.unpack_from('>4sIIII', result, 44 + i * 20)
        payload = result[offset:offset + compressed_length]
        data = zlib.decompress(payload) if compressed_length < length else payload
        assert len(data) == length
        decoded[tag] = data
    # Covers all original tables, including copyright/license/name/variation data.
    assert decoded == original
    return result, count


if __name__ == '__main__':
    destination = ROOT / 'fonts'
    destination.mkdir(exist_ok=True)
    for upstream, filename, expected in SOURCES:
        url = f'https://raw.githubusercontent.com/google/fonts/{COMMIT}/' + quote(upstream, safe='/')
        with urlopen(url, timeout=30) as response:
            source = response.read()
        assert hashlib.sha256(source).hexdigest() == expected, upstream
        result, count = package(source)
        (destination / filename).write_bytes(result)
        print(filename, len(result), 'bytes;', count, 'unchanged tables; source SHA-256 verified')
