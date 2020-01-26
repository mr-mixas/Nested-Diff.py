import pytest

from nested_diff import patch

from tests.data import standard, specific


TESTS = {}
TESTS.update(standard.get_tests())
TESTS.update(specific.get_tests())


@pytest.mark.parametrize('name', sorted(TESTS.keys()))
def test_patch(name):
    diff = TESTS[name]['diff']
    target = TESTS[name]['a']

    try:
        expected = TESTS[name]['patched']
    except KeyError:
        expected = TESTS[name]['b']

    assert expected == patch(target, diff)


# Test what doesn't covered by standard tests

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
