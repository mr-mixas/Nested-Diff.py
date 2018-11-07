from nested_diff import patch


def test_init():
    try:
        patch({}, {})
    except NotImplementedError:
        return 1

    raise Exception("Should be NotImplementedError here")
