import pytest

from nested_diff import Iterator, diff


def test_scalar_diff():
    a = 0
    b = 1

    expected = [(0, None, None, {'N': 1, 'O': 0})]
    got = list(Iterator().iterate(diff(a, b)))

    assert expected == got


def test_dict_diff():
    a = {'1': 1, '2': {'9': 9, '10': 10}, '3': 3}
    b = {'1': 1, '2': {'9': 8, '10': 10}, '4': 4}

    expected = [
        (0, None, None, {'D': {'1': {'U': 1}, '3': {'R': 3}, '2': {'D': {'9': {'N': 8, 'O': 9}, '10': {'U': 10}}}, '4': {'A': 4}}}),
        (1, dict, '1', {'U': 1}),
        (1, dict, '2', {'D': {'9': {'N': 8, 'O': 9}, '10': {'U': 10}}}),
        (2, dict, '10', {'U': 10}),
        (2, dict, '9', {'N': 8, 'O': 9}),
        (1, dict, '3', {'R': 3}),
        (1, dict, '4', {'A': 4}),
    ]

    got = list(Iterator().iterate(diff(a, b)))

    for i in expected:
        assert i in got

    assert len(got) == 7


def test_dict_diff_keys_sorted():
    a = {'1': 1, '2': {'9': 9, '10': 10}, '3': 3}
    b = {'1': 1, '2': {'9': 8, '10': 10}, '4': 4}

    expected = [
        (0, None, None, {'D': {'1': {'U': 1}, '3': {'R': 3}, '2': {'D': {'9': {'N': 8, 'O': 9}, '10': {'U': 10}}}, '4': {'A': 4}}}),
        (1, dict, '1', {'U': 1}),
        (1, dict, '2', {'D': {'9': {'N': 8, 'O': 9}, '10': {'U': 10}}}),
        (2, dict, '10', {'U': 10}),
        (2, dict, '9', {'N': 8, 'O': 9}),
        (1, dict, '3', {'R': 3}),
        (1, dict, '4', {'A': 4}),
    ]

    got = list(Iterator(sort_keys=True).iterate(diff(a, b)))

    assert expected == got


def test_list_diff():
    a = [0, [1], 3]
    b = [0, [1, 2], 3]

    expected = [
        (0, None, None, {'D': [{'U': 0}, {'D': [{'U': 1}, {'A': 2}]}, {'U': 3}]}),
        (1, list, 0, {'U': 0}),
        (1, list, 1, {'D': [{'U': 1}, {'A': 2}]}),
        (2, list, 0, {'U': 1}),
        (2, list, 1, {'A': 2}),
        (1, list, 2, {'U': 3}),
    ]

    got = list(Iterator().iterate(diff(a, b)))

    assert expected == got


def test_list_diff_noU():
    a = [0, [1], 3]
    b = [0, [1, 2], 3]

    expected = [
        (0, None, None, {'D': [{'D': [{'A': 2, 'I': 1}], 'I': 1}]}),
        (1, list, 1, {'D': [{'A': 2, 'I': 1}], 'I': 1}),
        (2, list, 1, {'A': 2, 'I': 1}),
    ]

    got = list(Iterator().iterate(diff(a, b, U=False)))

    assert expected == got


def test_set_diff():
    a = {0, 1}
    b = {0, 2}

    got = list(Iterator().iterate(diff(a, b)))

    assert [(0, None, None, {'E': set(), 'D': [{'U': 0}, {'R': 1}, {'A': 2}]})] == got


def test_custom_containers():
    class custom_container(tuple):
        pass

    diff = {'D': custom_container([{'O': 0, 'N': 1}])}

    it = Iterator()
    it.set_iter(custom_container, it._iter_sequence)

    expected = [
        (0, None, None, {'D': ({'N': 1, 'O': 0},)}),
        (1, custom_container, 0, {'N': 1, 'O': 0})
    ]

    got = list(it.iterate(diff))

    assert expected == got


def test_unknown_containers():
    class unknown_container(tuple):
        pass

    diff = {'D': unknown_container([{'O': 0, 'N': 1}])}

    with pytest.raises(NotImplementedError):
        list(Iterator().iterate(diff))
