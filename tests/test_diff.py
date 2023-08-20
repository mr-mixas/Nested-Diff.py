import pytest

from nested_diff import Differ, diff, handlers

from tests.data import specific, standard

TESTS = {}
TESTS.update(standard.get_tests())
TESTS.update(specific.get_tests())


@pytest.mark.parametrize('name', sorted(TESTS.keys()))
def test_diff(name):
    try:
        if TESTS[name]['skip']['diff']['cond']:
            pytest.skip(TESTS[name]['skip']['diff'].get('reason', ''))
    except KeyError:
        pass

    a = TESTS[name]['a']
    b = TESTS[name]['b']

    expected = TESTS[name]['diff']
    differ = Differ(**TESTS[name].get('diff_opts', {}))

    for handler, handler_opts in TESTS[name].get('handlers', {}).items():
        differ.set_handler(handler(**handler_opts))

    _, got = differ.diff(a, b)

    try:
        assert TESTS[name]['assert_func'](got, expected)
    except KeyError:
        assert got == expected


def test_local_objects():
    def local_function_cant_be_pickled():
        pass

    a = [local_function_cant_be_pickled]
    b = []

    with pytest.raises(Exception, match="Can't pickle"):  # noqa B017 (different exceptions on different python vers)
        Differ().diff(a, b)


class SubclassedDict(dict):
    # can't be declared inside test (Can't pickle local object)
    pass


def test_nested_derivatives():
    original = {}
    a = {'k': original}
    derivative = SubclassedDict()
    b = {'k': derivative}

    expected = {'D': {'k': {'N': derivative, 'O': original}}}
    _, got = Differ().diff(a, b)

    assert got == expected


def test_different_object_attributes():
    a = SubclassedDict()
    a.arbitrary_attr = True
    b = SubclassedDict()
    b.arbitrary_attr = False

    expected = {'N': b, 'O': a}
    _, got = Differ().diff(a, b)

    assert got == expected


def test_dicts_with_same_data_but_different_sequence_u_disabled():
    # for example pickle.dumps({1: 1, 2: 2}) != pickle.dumps({2: 2, 1: 1})
    a = {1: 1, 2: 2}
    b = {2: 2, 1: 1}

    expected = {}
    _, got = Differ(U=False).diff(a, b)

    assert got == expected


def test_dicts_with_same_data_but_different_sequence_u_enabled():
    # for example pickle.dumps({1: 1, 2: 2}) != pickle.dumps({2: 2, 1: 1})
    a = {1: 1, 2: 2}
    b = {2: 2, 1: 1}

    expected = {'U': {1: 1, 2: 2}}
    _, got = Differ(U=True).diff(a, b)

    assert got == expected


def test_dicts_with_same_data_but_different_sequence_in_list_u_enabled():
    a = [{1: 1, 2: 2}]
    b = [{2: 2, 1: 1}]

    expected = {'U': [{1: 1, 2: 2}]}
    _, got = Differ(U=True).diff(a, b)

    assert got == expected


def test_text_diff_func_extra_handlers_opt():
    a = ['a']
    b = ['a\nb']

    expected = {'D': [{'D': [{'I': [0, 1, 0, 2]}, {'U': 'a'}, {'A': 'b'}], 'E': 5}]}
    got = diff(a, b, extra_handlers=[handlers.TextHandler(context=3)])

    assert got == expected
