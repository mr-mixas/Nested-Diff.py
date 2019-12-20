import pytest

from nested_diff import patch


def test_incorrect_diff_type():
    with pytest.raises(TypeError):
        patch(None, None)


def test_type_mismatch():
    with pytest.raises(AttributeError):
        patch({}, {'D': [{'A': 1}]})


def test_unsupported_patch_type():
    class Foo(object):
        pass

    with pytest.raises(NotImplementedError):
        patch(None, {'D': Foo()})


def test_patch_set():
    a = {1, 2, 4, 5}
    b = {0, 1, 2, 3}

    ndiff = {
        'D': [
            {'A': 0},
            {'U': 1},
            {'U': 2},
            {'A': 3},
            {'R': 4},
            {'R': 5},
        ],
        'E': set(),
    }

    assert b == patch(a, ndiff)


def test_patch_frozenset():
    a = frozenset((1, 2))
    b = frozenset((2, 3))

    ndiff = {
        'D': [
            {'R': 1},
            {'U': 2},
            {'A': 3},
        ],
        'E': frozenset(),
    }

    assert b == patch(a, ndiff)


def test_patch_tuple():
    a = (1, 2, 4, 5)
    b = (0, 1, 2, 3)

    ndiff = {'D': ({'A': 0}, {'I': 2, 'N': 3}, {'R': 5})}

    assert b == patch(a, ndiff)
