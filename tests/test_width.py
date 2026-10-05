from pathlib import Path

import pytest

from ocodo_font_bitmap.width import fixed_width


def test_fixed_width_returns_positive(test_font: Path) -> None:
    width = fixed_width(font=test_font, height=32)
    assert width > 0
