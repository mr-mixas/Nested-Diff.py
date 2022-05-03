from nested_diff import Differ, handlers


def test_diff_handlers():
    class FloatHanler(handlers.TypeHandler):
        handled_type = float

        def __init__(self, precision=2, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.precision = precision

        def diff(self, differ, a, b):
            if round(a, self.precision) == round(b, self.precision):
                return {'U': a} if differ.op_u else {}

            return super().diff(differ, a, b)

    differ = Differ(U=False)
    differ.set_handler(FloatHanler(precision=1))

    a = [0.001, 0.01, 0.1]
    b = [0.002, 0.02, 0.2]

    assert {'D': [{'I': 2, 'N': 0.2, 'O': 0.1}]} == differ.diff(a, b)


# TODO: rename this file when handlers related deprecation cycle ended
# TODO: drop code below when handlers related deprecation cycle ended

def test_subclassing():
    class CustomDiffer(Differ):
        """Differ with custom precision for floats."""

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
