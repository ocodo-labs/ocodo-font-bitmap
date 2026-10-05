from pathlib import Path

import pytest

FONT_DIR = Path(__file__).parent / "fonts"


@pytest.fixture
def test_font() -> Path:
    return FONT_DIR / "3270-Regular.ttf"
