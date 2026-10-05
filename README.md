
# ocodo-font-bitmap

Generate Linux PSF2 bitmap console fonts from a TTF.

Used as a GitHub-based dependency by Ocodo font projects.

## Install

In a consuming project's `pyproject.toml`:

```toml
[project]
dependencies = [
    "ocodo-font-bitmap @ git+https://github.com/ocodo-labs/ocodo-font-bitmap.git@v0.1.0",
]
```

Or in a PEP 723 script:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "ocodo-font-bitmap @ git+https://github.com/ocodo-labs/ocodo-font-bitmap.git@v0.1.0",
# ]
# ///
```

## Usage

Generate a single bitmap font at a given pixel height:

```
ocodo-bitmap <height>
```

Font path, output slug, and output directory are resolved from `--font`, `--slug`, `--out`, or from `[tool.ocodo-font]` in the consuming project's `pyproject.toml`.

```toml
[tool.ocodo-font]
font = "~/.local/share/fonts/OcodoMonoDotZero-Light.ttf"
slug = "ocodo-mono-dotzero"
out = "dist"
```

CLI flags override config values.

### Options

```
--font PATH       Path to the source TTF
--slug STRING     Output filename prefix, e.g. ocodo-mono-dotzero
--out PATH        Output directory (default: dist)
--glyph-count N   Number of glyph slots (default: 512)
```

Output is written as `{out}/{slug}-{width}x{height}.psfu`, where `width` is derived from the font metrics at the requested height.

## License

MIT
