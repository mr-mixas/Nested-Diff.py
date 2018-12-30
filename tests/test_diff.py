from nested_diff import diff, _hdict


## Test what doesn't covered by external (JSON based) tests

def test_frozensets_diff():
    a = frozenset((1, 2))
    b = frozenset((2, 3))

    expected = {
        'D': frozenset((
            _hdict('R', 1),
            _hdict('U', 2),
            _hdict('A', 3),
        ))
    }

    assert expected == diff(a, b)


def test_sets_diff():
    a = {1, 2}
    b = {2, 3}

    expected = {
        'D': set((
            _hdict('R', 1),
            _hdict('U', 2),
            _hdict('A', 3),
        ))
    }

    assert expected == diff(a, b)


def test_sets_diff_noAR():
    a = {1, 2}
    b = {2, 3}

    expected = {
        'D': set((
            _hdict('U', 2),
        ))
    }

    assert expected == diff(a, b, A=False, R=False)


def test_sets_diff_noU():
    a = {1, 2}
    b = {2, 3}

    expected = {
        'D': set((
            _hdict('R', 1),
            _hdict('A', 3),
        ))
    }

    assert expected == diff(a, b, U=False)


def test_sets_diff_trimR():
    a = {1, 2}
    b = {2, 3}

    expected = {
        'D': set((
            _hdict('R', None),
            _hdict('U', 2),
            _hdict('A', 3),
        ))
    }

    assert expected == diff(a, b, trimR=True)


def test_sets_diff_empty_diff():
    a = {1, 2}
    b = {1, 2, 3}

    assert {} == diff(a, b, A=False, U=False)


def test_tuples_diff():
    a = (1, 2, 4, 5)
    b = (0, 1, 2, 3)

    assert {'D': ({'A': 0}, {'I': 2, 'N': 3}, {'R': 5})} == \
        diff(a, b, O=False, U=False)
