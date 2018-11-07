from nested_diff import diff

def test_diff_0_0():
    assert diff(0, 0) == {'U': 0}


def test_diff_0_1():
    assert diff(0, 1) == {'N': 1, 'O': 0}


def test_diff_empty_dicts():
    assert diff({}, {}) == {'U': {}}


def test_diff_equal_dicts():
    assert diff(
        {'one': 1, 'two': 2},
        {'two': 2, 'one': 1}
    ) == {'U': {'one': 1, 'two': 2}}


def test_diff_dicts_with_different_values():
    assert diff(
        {'one': 1, 'two': 2},
        {'one': 1, 'two': 0}
    ) == {'D': {'one': {'U': 1}, 'two': {'N': 0, 'O': 2}}}


def test_diff_dicts_with_different_keys():
    assert diff(
        {'one': 1, 'two': 2},
        {'one': 1, 'three': 3}
    ) == {'D': {'one': {'U': 1}, 'three': {'A': 3}, 'two': {'R': 2}}}


def test_diff_empty_lists():
    assert diff([], []) == {'U': []}


def test_diff_dics_vs_list():
    assert diff({}, []) == {'N': [], 'O': {}}


def test_diff_dics_vs_true():
    assert diff({}, True) == {'N': True, 'O': {}}

