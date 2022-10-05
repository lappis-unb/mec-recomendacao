
import pytest


def test_simple():
    assert 2 == 1 + 1

def test_throws():
    with pytest.raises(Exception) as e:
        1 / 0
    assert str(e.value) == 'division by zero'