import pytest

from nested_diff import patch, _hdict


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
        'D': set((
            _hdict('A', 0),
            _hdict('U', 1),
            _hdict('U', 2),
            _hdict('A', 3),
            _hdict('R', 4),
            _hdict('R', 5),
        ))
    }

    assert b == patch(a, ndiff)


def test_patch_frozenset():
    a = frozenset((1, 2))
    b = frozenset((2, 3))

    ndiff = {
        'D': frozenset((
            _hdict('R', 1),
            _hdict('U', 2),
            _hdict('A', 3),
        ))
    }

    assert b == patch(a, ndiff)


def test_patch_tuple():
    a = (1, 2, 4, 5)
    b = (0, 1, 2, 3)

    ndiff = {'D': ({'A': 0}, {'I': 2, 'N': 3}, {'R': 5})}

    assert b == patch(a, ndiff)
