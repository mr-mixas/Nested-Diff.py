from nested_diff import patch


def test_init():
    assert patch([], {}) == []
