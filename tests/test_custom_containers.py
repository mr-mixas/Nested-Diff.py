from nested_diff import Differ, Patcher
from nested_diff.handlers import TypeHandler


class CustomContainer():
    data = None


class CustomTypeHandler(TypeHandler):
    handled_type = CustomContainer

    def diff(self, differ, a, b):
        equal, diff = differ.diff(a.data, b.data)

        if 'D' in diff:
            cont = CustomContainer()
            cont.data = diff.pop('D')
            diff['D'] = cont

        if 'N' in diff:
            diff['N'] = b

        if 'O' in diff:
            diff['O'] = a

        return equal, diff

    def patch(self, patcher, target, diff):
        if 'D' in diff:
            diff['D'] = diff['D'].data

        target.data = patcher.patch(target.data, diff)

        return target


def test_deeply_different():
    old = CustomContainer()
    old.data = ['I', 'am', 'old', 'obj']

    new = CustomContainer()
    new.data = ['I', 'am', 'new', 'obj']

    differ = Differ(U=False)
    differ.set_handler(CustomTypeHandler())
    equal, diff = differ.diff(old, new)
    assert equal is False
    assert diff['D'].data == [{'I': 2, 'N': 'new', 'O': 'old'}]

    patcher = Patcher()
    patcher.set_handler(CustomTypeHandler())
    old = patcher.patch(old, diff)
    assert new.data == old.data


def test_entire_different():
    old = CustomContainer()
    old.data = ['old', 'obj']

    new = CustomContainer()
    new.data = {'new': 'obj'}

    differ = Differ(U=False)
    differ.set_handler(CustomTypeHandler())
    equal, diff = differ.diff(old, new)
    assert equal is False
    assert diff == {'O': old, 'N': new}

    patcher = Patcher()
    patcher.set_handler(CustomTypeHandler())
    old = patcher.patch(old, diff)
    assert new.data == old.data
