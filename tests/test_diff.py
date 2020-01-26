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


# Test what doesn't covered by batch tests above

def test_multiline_str_diff():
    a = 'one\ntwo\nthree'
    b = 'one\n2\nthree\n'

    expected = {
        'D': [
            {'I': [0, 3, 0, 4]},
            {'U': 'one'},
            {'R': 'two'},
            {'A': '2'},
            {'U': 'three'},
            {'A': ''},
        ],
        'E': '',
    }

    assert expected == diff(a, b, multiline_diff_context=3)
