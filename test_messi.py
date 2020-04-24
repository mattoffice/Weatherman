# test_capitalize.py
import pytest


def test_adds_3_and_3():
    # arrange
    expected = 6
    # act
    result = sum((3, 3))
    # assert
    assert expected == result
