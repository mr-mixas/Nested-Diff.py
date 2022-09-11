from nested_diff import Differ, handlers


def test_diff_handlers():
    class FloatHanler(handlers.TypeHandler):
        handled_type = float

        def __init__(self, precision=2, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.precision = precision

        def diff(self, differ, a, b):
            if round(a, self.precision) == round(b, self.precision):
                return True, {'U': a} if differ.op_u else {}

            return super().diff(differ, a, b)

    differ = Differ(U=False)
    differ.set_handler(FloatHanler(precision=1))

    a = [0.001, 0.01, 0.1]
    b = [0.002, 0.02, 0.2]

    assert (False, {'D': [{'I': 2, 'N': 0.2, 'O': 0.1}]}) == differ.diff(a, b)
