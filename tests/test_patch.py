import pytest

from nested_diff import Differ, Patcher, patch

from tests.data import specific, standard

TESTS = {}
TESTS.update(standard.get_tests())
TESTS.update(specific.get_tests())


@pytest.mark.parametrize('name', sorted(TESTS.keys()))
def test_patch(name):
    target = TESTS[name]['a']

    try:
        expected = TESTS[name]['patched']
    except KeyError:
        expected = TESTS[name]['b']

    got = Patcher().patch(target, TESTS[name]['diff'])

    try:
        assert TESTS[name]['assert_func'](got, expected)
    except KeyError:
        assert not Differ(U=False).diff(expected, got)[1]


# Test what doesn't covered by standard tests

def test_incorrect_diff_type():
    with pytest.raises(TypeError, match='is not iterable'):
        Patcher().patch(None, None)


def test_text_removing_line_mismatch():
    with pytest.raises(ValueError, match='Removing line does not match'):
        Patcher().patch(
            '\nB',
            {'D': [{'I': [0, 2, 0, 1]}, {'U': ''}, {'R': 'A'}], 'E': 5},
        )


def test_text_unchanged_line_mismatch():
    with pytest.raises(ValueError, match='Unchanged line does not match'):
        Patcher().patch(
            'A\nB',
            {'D': [{'I': [0, 2, 0, 1]}, {'U': 'Z'}, {'R': 'B'}], 'E': 5},
        )


def test_text_unsupported_op():
    with pytest.raises(ValueError, match='Unsupported operation'):
        Patcher().patch(
            'A\nB',
            {'D': [{'I': [0, 2, 0, 1]}, {'Z': 'A'}, {'R': 'B'}], 'E': 5},
        )


def test_incorrect_diff_format():
    with pytest.raises(ValueError, match="{'garbage': 'passed'}"):
        Patcher().patch({}, {'garbage': 'passed'})


def test_type_mismatch():
    with pytest.raises(AttributeError, match='has no attribute'):
        Patcher().patch({}, {'D': [{'A': 1}]})


def test_unsupported_extension():
    with pytest.raises(ValueError, match='unsupported extension: _ext_id_'):
        Patcher().patch(None, {'D': None, 'E': '_ext_id_'})


def test_unsupported_patch_type():
    with pytest.raises(ValueError, match='unsupported patch type: module'):
        Patcher().patch(None, {'D': pytest})  # module


def test_patch_func():
    assert patch('a', {'N': 'b', 'O': 'a'}) == 'b'
