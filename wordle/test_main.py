import pytest
from main import color_word
from main import GREEN_PAIR
from main import YELLOW_PAIR


@pytest.mark.parametrize(
    ("word", "guess", "expected"),
    (
        ("nymph", "world", []),
        ("trade", "hello", [(YELLOW_PAIR, 1)]),
        ("hauls", "hello", [(GREEN_PAIR, 0), (GREEN_PAIR, 3)]),
        ("slosh", "hello", [(YELLOW_PAIR, 0), (YELLOW_PAIR, 2), (YELLOW_PAIR, 4)]),
    ),
)
def test_color_word(word, guess, expected):
    assert color_word(word, guess) == expected
