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


def test_local_objects():
    def local_function_cant_be_pickled():
        pass

    a = [local_function_cant_be_pickled]
    b = []

    with pytest.raises(Exception):  # Can't pickle local object
        diff(a, b)


class SubclassedDict(dict):
    # can't be declared inside test (Can't pickle local object)
    pass


def test_nested_derivatives():
    original = {}
    a = {'k': original}
    derivative = SubclassedDict()
    b = {'k': derivative}

    d = diff(a, b)

    assert {'D': {'k': {'N': derivative, 'O': original}}} == d


def test_different_object_attributes():
    a = SubclassedDict()
    a.arbitrary_attr = True
    b = SubclassedDict()
    b.arbitrary_attr = False

    d = diff(a, b)

    assert {'N': b, 'O': a} == d


def test_str_multiline_diff_disabled_when_ON_disabled():  # noqa N802
    a = ['a']
    b = ['a\nb']

    assert {'D': [{'O': 'a'}]} == diff(a, b, N=False, multiline_diff_context=3)
    assert {'D': [{'N': 'a\nb'}]} == diff(a, b, O=False, multiline_diff_context=3)
    assert {} == diff(a, b, N=False, O=False, multiline_diff_context=3)
