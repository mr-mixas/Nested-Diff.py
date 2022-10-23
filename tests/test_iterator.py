from nested_diff import Iterator, diff


def test_scalar_diff():
    a = 0
    b = 1
    d = diff(a, b)

    expected = [(d, None, None)]
    got = list(Iterator().iterate(d))

    assert got == expected


def test_dict_diff():
    a = {'1': 1, '2': {'9': 9, '10': 10}, '3': 3}
    b = {'1': 1, '2': {'9': 8, '10': 10}, '4': 4}
    d = diff(a, b)

    expected = [
        (d, '1', d['D']['1']),
        (d['D']['1'], None, None),

        (d, '2', d['D']['2']),
        (d['D']['2'], '10', d['D']['2']['D']['10']),
        (d['D']['2']['D']['10'], None, None),
        (d['D']['2'], '9', d['D']['2']['D']['9']),
        (d['D']['2']['D']['9'], None, None),

        (d, '3', d['D']['3']),
        (d['D']['3'], None, None),

        (d, '4', d['D']['4']),
        (d['D']['4'], None, None),
    ]

    got = list(Iterator().iterate(d))

    for i in expected:
        assert i in got

    assert len(got) == 11


def test_dict_diff__keys_sorted():
    a = {'1': 1, '2': {'9': 9, '10': 10}, '3': 3}
    b = {'1': 1, '2': {'9': 8, '10': 10}, '4': 4}
    d = diff(a, b)

    expected = [
        (d, '1', d['D']['1']),
        (d['D']['1'], None, None),

        (d, '2', d['D']['2']),
        (d['D']['2'], '10', d['D']['2']['D']['10']),
        (d['D']['2']['D']['10'], None, None),
        (d['D']['2'], '9', d['D']['2']['D']['9']),
        (d['D']['2']['D']['9'], None, None),

        (d, '3', d['D']['3']),
        (d['D']['3'], None, None),

        (d, '4', d['D']['4']),
        (d['D']['4'], None, None),
    ]

    got = list(Iterator(sort_keys=True).iterate(d))

    assert got == expected


def test_list_diff():
    a = [0, [1], 3]
    b = [0, [1, 2], 3]
    d = diff(a, b)

    expected = [
        (d, 0, d['D'][0]),
        (d['D'][0], None, None),

        (d, 1, d['D'][1]),
        (d['D'][1], 0, d['D'][1]['D'][0]),
        (d['D'][1]['D'][0], None, None),
        (d['D'][1], 1, d['D'][1]['D'][1]),
        (d['D'][1]['D'][1], None, None),

        (d, 2, d['D'][2]),
        (d['D'][2], None, None)]

    got = list(Iterator().iterate(d))

    assert got == expected


def test_list_diff__noU():  # noqa N802
    a = [0, [1], 3]
    b = [0, [1, 2], 3]
    d = diff(a, b, U=False)

    expected = [
        (d, 1, d['D'][0]),
        (d['D'][0], 1, d['D'][0]['D'][0]),
        (d['D'][0]['D'][0], None, None),
    ]

    got = list(Iterator().iterate(d))

    assert got == expected


def test_set_diff():
    a = {0, 1}
    b = {0, 2}
    d = diff(a, b)

    expected = [
        ({'D': [{'U': 0}, {'R': 1}, {'A': 2}], 'E': 3}, None, None),
    ]

    got = list(Iterator().iterate(d))

    assert got == expected


def test_unknown_containers():
    class UnknownContainer(tuple):
        pass

    d = {'D': UnknownContainer([{'O': 0, 'N': 1}])}

    expected = [(d, None, None)]  # final (not iterated)

    got = list(Iterator().iterate(d))

    assert got == expected
