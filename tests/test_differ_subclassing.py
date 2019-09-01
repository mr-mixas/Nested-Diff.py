from nested_diff import Differ


def test_subclassing():
    class CustomDiffer(Differ):
        """
        Use custom precision for floats.

        """
        def __init__(self, float_precision=2, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_differ(float, self.diff_float)
            self.float_precision = float_precision

        def diff_float(self, a, b):
            if round(a, self.float_precision) == round(b, self.float_precision):
                return {'U': a} if self.op_u else {}

            return super().diff__default(a, b)

    differ = CustomDiffer(float_precision=1, U=False)

    a = [0.001, 0.01, 0.1]
    b = [0.002, 0.02, 0.2]

    assert {'D': [{'I': 2, 'N': 0.2, 'O': 0.1}]} == differ.diff(a, b)
