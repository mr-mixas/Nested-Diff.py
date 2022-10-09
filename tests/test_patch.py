import pytest

from nested_diff import diff, patch

from tests.data import standard, specific

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

    got = patch(target, TESTS[name]['diff'])

    assert not diff(expected, got, U=False)


# Test what doesn't covered by standard tests

def test_incorrect_diff_type():
    with pytest.raises(TypeError):
        patch(None, None)


def test_text_removing_line_mismatsh():
    with pytest.raises(ValueError):
        patch(
            '\nB',
            {'D': [{'I': [0, 2, 0, 1]}, {'U': ''}, {'R': 'A'}], 'E': ''},
        )


def test_text_unchanged_line_mismatsh():
    with pytest.raises(ValueError):
        patch(
            'A\nB',
            {'D': [{'I': [0, 2, 0, 1]}, {'U': 'Z'}, {'R': 'B'}], 'E': ''},
        )


def test_text_unsupported_op():
    with pytest.raises(ValueError):
        patch(
            'A\nB',
            {'D': [{'I': [0, 2, 0, 1]}, {'Z': 'A'}, {'R': 'B'}], 'E': ''},
        )


def test_incorrect_diff_format():
    with pytest.raises(ValueError):
        patch({}, {'garbage': 'passed'})


def test_type_mismatch():
    with pytest.raises(AttributeError):
        patch({}, {'D': [{'A': 1}]})


def test_unsupported_patch_type():
    with pytest.raises(ValueError):
        patch(None, {'D': pytest})  # module
