from nested_diff import Walker, diff, _hdict


def test_walk_dict():
    a = {'1': 1, '2': {'9': 9, '10': 10}, '3': 3}
    b = {'1': 1, '2': {'9': 8, '10': 10}, '4': 4}

    expected = [
        (0, None, {'D': {'1': {'U': 1}, '3': {'R': 3}, '2': {'D': {'9': {'N': 8, 'O': 9}, '10': {'U': 10}}}, '4': {'A': 4}}}),
        (1, '1', {'U': 1}),
        (1, '2', {'D': {'9': {'N': 8, 'O': 9}, '10': {'U': 10}}}),
        (2, '10', {'U': 10}),
        (2, '9', {'N': 8, 'O': 9}),
        (1, '3', {'R': 3}),
        (1, '4', {'A': 4}),
    ]

    got = list(Walker().walk(diff(a, b)))

    for i in expected:
        assert i in got

    assert len(got) == 7


def test_walk_dict_keys_sorted():
    a = {'1': 1, '2': {'9': 9, '10': 10}, '3': 3}
    b = {'1': 1, '2': {'9': 8, '10': 10}, '4': 4}

    expected = [
        (0, None, {'D': {'1': {'U': 1}, '3': {'R': 3}, '2': {'D': {'9': {'N': 8, 'O': 9}, '10': {'U': 10}}}, '4': {'A': 4}}}),
        (1, '1', {'U': 1}),
        (1, '2', {'D': {'9': {'N': 8, 'O': 9}, '10': {'U': 10}}}),
        (2, '10', {'U': 10}),
        (2, '9', {'N': 8, 'O': 9}),
        (1, '3', {'R': 3}),
        (1, '4', {'A': 4}),
    ]

    got = list(Walker(sort_keys=True).walk(diff(a, b)))

    assert expected == got


def test_walk_list():
    a = [0, [1], 3]
    b = [0, [1, 2], 3]

    expected = [
        (0, None, {'D': [{'U': 0}, {'D': [{'U': 1}, {'A': 2}]}, {'U': 3}]}),
        (1, 0, {'U': 0}),
        (1, 1, {'D': [{'U': 1}, {'A': 2}]}),
        (2, 0, {'U': 1}),
        (2, 1, {'A': 2}),
        (1, 2, {'U': 3}),
    ]

    got = list(Walker().walk(diff(a, b)))

    assert expected == got


def test_walk_set():
    a = {0, 1}
    b = {0, 2}

    got = list(Walker().walk(diff(a, b)))

    assert len(got) == 4
    assert got[0] == (0, None, {'D': {_hdict('R', 1), _hdict('A', 2), _hdict('U', 0)}})
    assert (1, None, {'R': 1}) in got
    assert (1, None, {'A': 2}) in got
    assert (1, None, {'U': 0}) in got
