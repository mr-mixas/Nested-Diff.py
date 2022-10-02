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

    assert got == expected


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

    expected = {'D': {'k': {'N': derivative, 'O': original}}}
    got = diff(a, b)

    assert got == expected


def test_different_object_attributes():
    a = SubclassedDict()
    a.arbitrary_attr = True
    b = SubclassedDict()
    b.arbitrary_attr = False

    expected = {'N': b, 'O': a}
    got = diff(a, b)

    assert got == expected


def test_text_diff_disabled_when_ON_disabled():  # noqa N802
    a = ['a']
    b = ['a\nb']

    assert diff(a, b, N=False, text_diff_ctx=3) == {'D': [{'O': 'a'}]}
    assert diff(a, b, O=False, text_diff_ctx=3) == {'D': [{'N': 'a\nb'}]}
    assert diff(a, b, N=False, O=False, text_diff_ctx=3) == {}


def test_dicts_with_same_data_but_different_sequence_u_disabled():
    # for example pickle.dumps({1: 1, 2: 2}) != pickle.dumps({2: 2, 1: 1})
    a = {1: 1, 2: 2}
    b = {2: 2, 1: 1}

    expected = {}
    got = diff(a, b, U=False)

    assert got == expected


def test_dicts_with_same_data_but_different_sequence_u_enabled():
    # for example pickle.dumps({1: 1, 2: 2}) != pickle.dumps({2: 2, 1: 1})
    a = {1: 1, 2: 2}
    b = {2: 2, 1: 1}

    expected = {'U': {1: 1, 2: 2}}
    got = diff(a, b, U=True)

    assert got == expected


def test_dicts_with_same_data_but_different_sequence_in_list_u_enabled():
    a = [{1: 1, 2: 2}]
    b = [{2: 2, 1: 1}]

    expected = {'U': [{1: 1, 2: 2}]}
    got = diff(a, b, U=True)

    assert got == expected
