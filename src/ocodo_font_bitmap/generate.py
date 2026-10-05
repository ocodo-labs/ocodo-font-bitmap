import argparse
import struct
import tomllib
from pathlib import Path

import freetype

from ocodo_font_bitmap.width import fixed_width

GLYPH_COUNT = 512


def load_config(root: Path = Path.cwd()) -> dict:
    pyproject = root / "pyproject.toml"

    if not pyproject.is_file():
        return {}

    with pyproject.open("rb") as fh:
        data = tomllib.load(fh)

    return data.get("tool", {}).get("ocodo-font", {})


def glyphs(face: freetype.Face):
    charcode, glyph_index = face.get_first_char()

    while glyph_index:
        yield charcode, glyph_index
        charcode, glyph_index = face.get_next_char(
            charcode,
            glyph_index,
        )


def rasterize(
    face: freetype.Face,
    glyph_index: int,
    width: int,
    height: int,
) -> bytes:
    face.load_glyph(
        glyph_index,
        freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO,
    )

    glyph = face.glyph
    bitmap = glyph.bitmap

    bearing_x = glyph.metrics.horiBearingX // 64
    bearing_y = glyph.metrics.horiBearingY // 64
    advance = glyph.advance.x // 64
    baseline = face.size.ascender // 64

    x = (width - advance) // 2 + bearing_x
    y = baseline - bearing_y

    pixels = bytearray(width * height)

    for row in range(bitmap.rows):
        py = y + row

        if not 0 <= py < height:
            continue

        for col in range(bitmap.width):
            px = x + col

            if not 0 <= px < width:
                continue

            source_byte = row * bitmap.pitch + col // 8
            source_bit = 7 - col % 8

            if bitmap.buffer[source_byte] & (1 << source_bit):
                pixels[py * width + px] = 1

    return bytes(pixels)


def psf2(
    bitmaps: list[bytes],
    codepoints: list[int | None],
    width: int,
    height: int,
    glyph_count: int,
) -> bytes:
    bytes_per_row = (width + 7) // 8
    bytes_per_glyph = bytes_per_row * height

    header = struct.pack(
        "<8I",
        0x864AB572,
        0,
        32,
        0x01,
        glyph_count,
        bytes_per_glyph,
        height,
        width,
    )

    bitmap_data = bytearray()

    for bitmap in bitmaps:
        for y in range(height):
            row = bitmap[y * width:(y + 1) * width]

            for start in range(0, width, 8):
                value = 0

                for bit in range(8):
                    x = start + bit

                    if x >= width:
                        break

                    if row[x]:
                        value |= 1 << (7 - bit)

                bitmap_data.append(value)

    unicode_data = bytearray()

    for codepoint in codepoints:
        if codepoint is not None:
            unicode_data.extend(chr(codepoint).encode("utf-8"))

        unicode_data.append(0xFF)

    return header + bytes(bitmap_data) + bytes(unicode_data)


def build(
    font: Path,
    height: int,
    out_dir: Path,
    slug: str,
    glyph_count: int = GLYPH_COUNT,
) -> Path:
    width = int(fixed_width(font=font, height=height))

    output = out_dir / f"{slug}-{width}x{height}.psfu"
    output.parent.mkdir(parents=True, exist_ok=True)

    face = freetype.Face(str(font))
    face.set_pixel_sizes(0, height)

    mapping = dict(glyphs(face))

    blank = bytes(width * height)

    bitmaps: list[bytes] = []
    codepoints: list[int | None] = []

    for slot in range(glyph_count):
        codepoint = slot if slot < 256 else None
        glyph_index = mapping.get(codepoint) if codepoint is not None else None

        if glyph_index is None:
            bitmaps.append(blank)
            codepoints.append(codepoint)
        else:
            bitmaps.append(rasterize(face, glyph_index, width, height))
            codepoints.append(codepoint)

    output.write_bytes(
        psf2(bitmaps, codepoints, width, height, glyph_count)
    )

    print(f"{width}x{height}")
    print(f"glyphs: {glyph_count}")
    print(f"output: {output}")

    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ocodo-bitmap",
        description="Generate a Linux PSF2 bitmap console font from a TTF.",
    )
    parser.add_argument("height", type=int)
    parser.add_argument("--font", type=Path)
    parser.add_argument("--slug", type=str)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--glyph-count", type=int)
    return parser.parse_args(argv)


def resolve(args: argparse.Namespace, config: dict) -> dict:
    font = args.font or (
        Path(config["font"]).expanduser() if "font" in config else None
    )
    slug = args.slug or config.get("slug")
    out_dir = args.out or Path(config.get("out", "dist"))
    glyph_count = args.glyph_count or config.get("glyph_count", GLYPH_COUNT)

    if font is None:
        raise SystemExit(
            "No font specified. Use --font or [tool.ocodo-font] font in pyproject.toml."
        )

    if slug is None:
        raise SystemExit(
            "No slug specified. Use --slug or [tool.ocodo-font] slug in pyproject.toml."
        )

    font = Path(font).expanduser()

    if not font.is_file():
        raise SystemExit(f"Font not found: {font}")

    return {
        "font": font,
        "slug": slug,
        "out_dir": out_dir,
        "glyph_count": glyph_count,
        "height": args.height,
    }


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    config = load_config()
    opts = resolve(args, config)

    build(
        font=opts["font"],
        height=opts["height"],
        out_dir=opts["out_dir"],
        slug=opts["slug"],
        glyph_count=opts["glyph_count"],
    )


if __name__ == "__main__":
    main()
