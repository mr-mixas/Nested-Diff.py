import pytest

from nested_diff import diff

from tests.data import standard, specific

TESTS = {}
TESTS.update(standard.get_tests())
TESTS.update(specific.get_tests())


@pytest.mark.parametrize('name', sorted(TESTS.keys()))
def test_diff(name):
    a = TESTS[name]['a']
    b = TESTS[name]['b']
    expected = TESTS[name]['diff']
    opts = TESTS[name].get('diff_opts', {})
    got = diff(a, b, **opts)

    assert expected == got
