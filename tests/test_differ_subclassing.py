from nested_diff import Differ


def test_subclassing2():
    class CustomDiffer(Differ):
        """
        Use custom precision for floats.

        """
        def __init__(self, *args, **kwargs):
            super(CustomDiffer, self).__init__(*args, **kwargs)
            self.set_differ(float, self.diff_float)

        def diff_float(self, a, b):
            if round(a, 1) == round(b, 1):
                return {'U': a} if self.op_u else {}

            return super(CustomDiffer, self).diff__default(a, b)

    differ = CustomDiffer(U=False)

    a = [0.001, 0.01, 0.1]
    b = [0.002, 0.02, 0.2]

    assert {'D': [{'I': 2, 'N': 0.2, 'O': 0.1}]} == differ.diff(a, b)
