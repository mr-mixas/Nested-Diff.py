import pytest

from nested_diff import patch


def test_incorrect_diff_type():
    with pytest.raises(TypeError):
        patch(None, None)


def test_type_mismatch():
    with pytest.raises(AttributeError):
        patch({}, {'D': [{'A': 1}]})


def test_unsupported_patch_type():
    with pytest.raises(NotImplementedError):
        patch(None, {'D': set({'A': 1})})


def test_patch_tuple():
    a = (1, 2, 4, 5)
    b = (0, 1, 2, 3)

    ndiff = {'D': ({'A': 0}, {'I': 2, 'N': 3}, {'R': 5})}

    assert b == patch(a, ndiff)
