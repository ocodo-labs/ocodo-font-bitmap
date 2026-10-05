import struct
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

import pytest

from ocodo_font_bitmap.generate import (
    GLYPH_COUNT,
    build,
    resolve,
)

PSF2_MAGIC = 0x864AB572


def make_args(
    height: int = 32,
    font: Path | None = None,
    slug: str | None = None,
    out: Path | None = None,
    glyph_count: int | None = None,
) -> Namespace:
    return Namespace(
        height=height,
        font=font,
        slug=slug,
        out=out,
        glyph_count=glyph_count,
    )


def test_build_writes_expected_file(test_font: Path, tmp_path: Path) -> None:
    out = build(
        font=test_font,
        height=32,
        out_dir=tmp_path,
        slug="ibm3270",
    )
    assert out.is_file()
    assert out.name.startswith("ibm3270-")
    assert out.name.endswith("x32.psfu")


def test_build_psf2_header(test_font: Path, tmp_path: Path) -> None:
    out = build(
        font=test_font,
        height=32,
        out_dir=tmp_path,
        slug="ibm3270",
    )
    data = out.read_bytes()
    (
        magic,
        version,
        header_size,
        flags,
        glyph_count,
        bytes_per_glyph,
        height,
        width,
    ) = struct.unpack("<8I", data[:32])
    assert magic == PSF2_MAGIC
    assert version == 0
    assert header_size == 32
    assert flags == 0x01
    assert glyph_count == GLYPH_COUNT
    assert height == 32
    assert width > 0
    assert bytes_per_glyph == ((width + 7) // 8) * height


def test_build_explicit_glyph_count(test_font: Path, tmp_path: Path) -> None:
    out = build(
        font=test_font,
        height=32,
        out_dir=tmp_path,
        slug="ibm3270",
        glyph_count=256,
    )
    data = out.read_bytes()
    _, _, _, _, glyph_count, _, _, _ = struct.unpack("<8I", data[:32])
    assert glyph_count == 256


def test_resolve_cli_args_win(test_font: Path, tmp_path: Path) -> None:
    args = make_args(
        height=32,
        font=test_font,
        slug="from-cli",
        out=tmp_path,
        glyph_count=1024,
    )
    config = {
        "font": "/nonexistent.ttf",
        "slug": "from-config",
        "out": "/tmp/elsewhere",
        "glyph_count": 512,
    }
    opts = resolve(args, config)
    assert opts["font"] == test_font
    assert opts["slug"] == "from-cli"
    assert opts["out_dir"] == tmp_path
    assert opts["glyph_count"] == 1024
    assert opts["height"] == 32


def test_resolve_config_used_when_cli_absent(
    test_font: Path, tmp_path: Path
) -> None:
    args = make_args(height=32)
    config = {
        "font": str(test_font),
        "slug": "from-config",
        "out": str(tmp_path),
        "glyph_count": 256,
    }
    opts = resolve(args, config)
    assert opts["font"] == test_font
    assert opts["slug"] == "from-config"
    assert opts["out_dir"] == tmp_path
    assert opts["glyph_count"] == 256


def test_resolve_defaults(test_font: Path) -> None:
    args = make_args(height=32, font=test_font, slug="s")
    opts = resolve(args, {})
    assert opts["out_dir"] == Path("dist")
    assert opts["glyph_count"] == GLYPH_COUNT


def test_resolve_config_font_expands_tilde(test_font: Path) -> None:
    args = make_args(height=32, slug="s")
    config = {"font": f"~/{test_font.relative_to(Path.home())}"}
    opts = resolve(args, config)
    assert opts["font"] == test_font


def test_resolve_missing_font_raises() -> None:
    args = make_args(height=32, slug="s")
    with pytest.raises(SystemExit):
        resolve(args, {})


def test_resolve_missing_slug_raises(test_font: Path) -> None:
    args = make_args(height=32, font=test_font)
    with pytest.raises(SystemExit):
        resolve(args, {})


def test_resolve_nonexistent_font_raises(tmp_path: Path) -> None:
    args = make_args(
        height=32,
        font=tmp_path / "nope.ttf",
        slug="s",
    )
    with pytest.raises(SystemExit):
        resolve(args, {})


def test_cli_end_to_end(test_font: Path, tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ocodo_font_bitmap.generate",
            "32",
            "--font",
            str(test_font),
            "--slug",
            "ibm3270",
            "--out",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert list(tmp_path.glob("ibm3270-*x32.psfu"))
