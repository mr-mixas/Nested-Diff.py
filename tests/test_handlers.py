from nested_diff import Differ, handlers


def test_diff_handlers():
    class FloatHandler(handlers.FloatHandler):
        def __init__(self, precision=2, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.precision = precision

        def diff(self, differ, a, b):
            if round(a, self.precision) == round(b, self.precision):
                return True, {'U': a} if differ.op_u else {}

            return super().diff(differ, a, b)

    differ = Differ(U=False)
    differ.set_handler(FloatHandler(precision=1))

    a = [0.001, 0.01, 0.1]
    b = [0.002, 0.02, 0.2]

    expected = (False, {'D': [{'I': 2, 'N': 0.2, 'O': 0.1}]})
    got = differ.diff(a, b)

    assert got == expected


def test_scalar_handler_diff_equal():
    a = 0
    b = 0

    expected = (True, {'U': 0})
    got = handlers.ScalarHandler().diff(Differ(), a, b)

    assert got == expected


def test_text_handler_diff_equal_noU():  # noqa N802
    a = '1\n2'
    b = '1\n2'

    expected = (True, {})
    got = handlers.TextHandler().diff(Differ(U=False), a, b)

    assert got == expected


def test_type_handler_diff_equal():
    a = 0
    b = 0

    expected = (True, {'U': 0})
    got = handlers.TypeHandler().diff(Differ(), a, b)

    assert got == expected
