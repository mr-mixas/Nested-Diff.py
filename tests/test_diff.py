from nested_diff import diff


def test_init():
    assert diff([], {}) == {}
