from nested_diff import Differ, Patcher


class CustomContainer(object):
    data = None


class CustomDiffer(Differ):
    def __init__(self, *args, **kwargs):
        super(CustomDiffer, self).__init__(*args, **kwargs)
        self.set_differ(CustomContainer, self.diff_custom_container)

    def diff_custom_container(self, a, b):
        diff = self.diff(a.data, b.data)

        if 'D' in diff:
            cont = CustomContainer()
            cont.data = diff.pop('D')
            diff['D'] = cont

        if 'N' in diff:
            diff['N'] = b

        if 'O' in diff:
            diff['O'] = a

        return diff


class CustomPatcher(Patcher):
    def __init__(self, *args, **kwargs):
        super(CustomPatcher, self).__init__(*args, **kwargs)
        self.set_patcher(CustomContainer, self.patch_custom_container)

    def patch_custom_container(self, target, ndiff):
        if 'D' in ndiff:
            ndiff['D'] = ndiff['D'].data

        target.data = self.patch(target.data, ndiff)

        return target


def test_deeply_different():
    old = CustomContainer()
    old.data = ['I', 'am', 'old', 'obj']

    new = CustomContainer()
    new.data = ['I', 'am', 'new', 'obj']

    diff = CustomDiffer(U=False).diff(old, new)
    assert [{'I': 2, 'N': 'new', 'O': 'old'}] == diff['D'].data

    old = CustomPatcher().patch(old, diff)
    assert old.data == new.data


def test_entire_different():
    old = CustomContainer()
    old.data = ['old', 'obj']

    new = CustomContainer()
    new.data = {'new': 'obj'}

    diff = CustomDiffer().diff(old, new)
    assert {'O': old, 'N': new} == diff

    old = CustomPatcher().patch(old, diff)
    assert old.data == new.data
