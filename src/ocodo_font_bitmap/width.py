from pathlib import Path

import freetype


def fixed_width(font: Path, height: int) -> float:
    face = freetype.Face(str(font))
    face.set_pixel_sizes(0, height)
    face.load_char(
        "A",
        freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO,
    )
    return face.glyph.advance.x / 64
