from nested_diff import diff, patch


class Custom(object):
    def __init__(self, value=None):
        self.value = value

    def __diff__(self, other, differ):
        dif = differ.diff(self.value, other.value)

        if 'U' in dif:
            return {'U': self}

        if dif:
            return {'D': self.__class__(value=dif)}

        return dif

    def __patch__(self, ndiff, patcher):
        if 'N' in ndiff:
            return ndiff['N']

        if 'D' in ndiff:
            self.value = patcher.patch(self.value, ndiff['D'].value)

        return self


def test_diff_different():
    a = Custom(value=0)
    b = Custom(value=1)

    result = diff(a, b, diff_method='__diff__')
    subdiff = result.pop('D')

    assert isinstance(subdiff, Custom)
    assert {'N': 1, 'O': 0} == subdiff.value
    assert {} == result


def test_diff_opts():
    a = Custom(value=0)
    b = Custom(value=1)

    result = diff(a, b, O=False, diff_method='__diff__')  # noqa: E741
    subdiff = result.pop('D')

    assert isinstance(subdiff, Custom)
    assert {'N': 1} == subdiff.value
    assert {} == result


def test_diff_equal():
    a = Custom(value=[0])
    b = Custom(value=[0])

    assert {'U': a} == diff(a, b, diff_method='__diff__')


def test_patch_with_diff_method():
    a = Custom(value=0)
    b = Custom(value=1)

    diff_ = diff(a, b, diff_method='__diff__')
    a = patch(a, diff_, patch_method='__patch__')

    assert isinstance(a, Custom)
    assert 1 == a.value


def test_patch_without_diff_method():
    a = Custom(value={'old': 0})
    b = Custom(value={'new': 1})

    diff_ = diff(a, b)
    a = patch(a, diff_, patch_method='__patch__')

    assert isinstance(a, Custom)
    assert {'new': 1} == a.value
