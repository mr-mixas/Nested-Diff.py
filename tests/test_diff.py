from nested_diff import diff


## Test what doesn't covered by external (JSON based) tests

def test_tuples_diff():
    a = (1, 2, 4, 5)
    b = (0, 1, 2, 3)

    assert {'D': ({'A': 0}, {'I': 2, 'N': 3}, {'R': 5})} == \
        diff(a, b, O=False, U=False)
