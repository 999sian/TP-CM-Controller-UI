#!/usr/bin/env python3
"""Export the mod's BTI artwork as PNG reference images.

The generated files live under extras/texture-bases/ and are intentionally
outside res/, so they are never packaged into the .dusk bundle.

Current TP Classic artwork uses GX RGB5A3 (BTI format 5). Conversion is a
pixel-for-pixel decode: no resizing, filtering, recoloring, or alpha editing.
"""

from __future__ import annotations

import argparse
import binascii
import io
import struct
import tarfile
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "extras" / "texture-bases"


def _expand5(v: int) -> int:
    return (v << 3) | (v >> 2)


def _expand4(v: int) -> int:
    return (v << 4) | v


def _expand3(v: int) -> int:
    return (v << 5) | (v << 2) | (v >> 1)


def decode_rgb5a3_bti(data: bytes) -> tuple[int, int, bytes]:
    if len(data) < 0x20:
        raise ValueError("BTI is smaller than its 0x20-byte header")

    fmt = data[0]
    if fmt != 5:
        raise ValueError(f"unsupported BTI format {fmt}; expected RGB5A3 (5)")

    width = struct.unpack_from(">H", data, 0x02)[0]
    height = struct.unpack_from(">H", data, 0x04)[0]
    image_offset = struct.unpack_from(">I", data, 0x1C)[0]

    block_count = ((width + 3) // 4) * ((height + 3) // 4)
    required = image_offset + block_count * 32
    if image_offset < 0x20 or required > len(data):
        raise ValueError("invalid RGB5A3 image range")

    rgba = bytearray(width * height * 4)
    pos = image_offset

    for by in range(0, height, 4):
        for bx in range(0, width, 4):
            for y in range(4):
                for x in range(4):
                    value = struct.unpack_from(">H", data, pos)[0]
                    pos += 2

                    if value & 0x8000:
                        a = 255
                        r = _expand5((value >> 10) & 0x1F)
                        g = _expand5((value >> 5) & 0x1F)
                        b = _expand5(value & 0x1F)
                    else:
                        a = _expand3((value >> 12) & 0x07)
                        r = _expand4((value >> 8) & 0x0F)
                        g = _expand4((value >> 4) & 0x0F)
                        b = _expand4(value & 0x0F)

                    px = bx + x
                    py = by + y
                    if px >= width or py >= height:
                        continue
                    out = (py * width + px) * 4
                    rgba[out:out + 4] = bytes((r, g, b, a))

    return width, height, bytes(rgba)


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    body = kind + payload
    return (
        struct.pack(">I", len(payload))
        + body
        + struct.pack(">I", binascii.crc32(body) & 0xFFFFFFFF)
    )


def encode_rgba_png(width: int, height: int, rgba: bytes) -> bytes:
    stride = width * 4
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # PNG filter type: None
        start = y * stride
        raw.extend(rgba[start:start + stride])

    return b"".join(
        (
            b"\x89PNG\r\n\x1a\n",
            _png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)),
            _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9)),
            _png_chunk(b"IEND", b""),
        )
    )


def direct_sources() -> list[tuple[Path, str]]:
    result: list[tuple[Path, str]] = []
    mappings = (
        (ROOT / "res" / "buttons", "playstation"),
        (ROOT / "res" / "xbox", "xbox"),
        (ROOT / "res" / "ornament", "ornaments"),
    )
    for folder, output_name in mappings:
        for path in sorted(folder.glob("*.bti")):
            result.append((path, f"{output_name}/{path.stem}.png"))

    guide = ROOT / "res" / "layout_guide.bti"
    if guide.exists():
        result.append((guide, "internal/layout_guide.png"))
    return result


def switch_sources() -> list[tuple[bytes, str, str]]:
    result: list[tuple[bytes, str, str]] = []
    seen: set[str] = set()

    for archive_path in sorted((ROOT / "assets" / "switch").glob("*.tar.gz")):
        with tarfile.open(archive_path, "r:gz") as archive:
            for member in archive.getmembers():
                if not member.isfile() or not member.name.lower().endswith(".bti"):
                    continue
                name = Path(member.name).name
                if name in seen:
                    raise ValueError(f"duplicate Switch BTI name: {name}")
                handle = archive.extractfile(member)
                if handle is None:
                    raise ValueError(f"could not read {member.name} from {archive_path.name}")
                seen.add(name)
                result.append((handle.read(), f"switch/{Path(name).stem}.png", archive_path.name))

    return sorted(result, key=lambda item: item[1])


def expected_pngs() -> dict[str, bytes]:
    generated: dict[str, bytes] = {}

    for path, output_path in direct_sources():
        width, height, rgba = decode_rgb5a3_bti(path.read_bytes())
        generated[output_path] = encode_rgba_png(width, height, rgba)

    for data, output_path, _archive in switch_sources():
        width, height, rgba = decode_rgb5a3_bti(data)
        generated[output_path] = encode_rgba_png(width, height, rgba)

    return generated


def write_all(expected: dict[str, bytes]) -> None:
    for path in sorted(OUT.rglob("*.png")) if OUT.exists() else []:
        path.unlink()

    for relative, data in expected.items():
        destination = OUT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)

    print(f"Exported {len(expected)} reference PNGs to {OUT.relative_to(ROOT)}")


def check_all(expected: dict[str, bytes]) -> int:
    actual = {
        str(path.relative_to(OUT)).replace("\\", "/"): path.read_bytes()
        for path in OUT.rglob("*.png")
    } if OUT.exists() else {}

    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    changed = sorted(path for path in expected.keys() & actual.keys() if expected[path] != actual[path])

    if missing or extra or changed:
        for label, paths in (("missing", missing), ("extra", extra), ("out of date", changed)):
            for path in paths:
                print(f"{label}: {path}")
        print("Run: python tools/export_texture_reference_pngs.py --write")
        return 1

    print(f"{len(expected)} texture reference PNGs are current")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="write the reference PNGs")
    mode.add_argument("--check", action="store_true", help="verify committed PNGs match the BTIs")
    args = parser.parse_args()

    expected = expected_pngs()
    if args.check:
        return check_all(expected)

    write_all(expected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
