from nested_diff import Differ


def test_subclassing():
    class CustomDiffer(Differ):
        """
        Diff floats using defined precision
        """
        def get_default_diff(self, a, b):
            if isinstance(a, float) and isinstance(a, type(b)):
                if round(a, 1) == round(b, 1):
                    return {'U': a} if self.op_u else {}

            return super(CustomDiffer, self).get_default_diff(a, b)

    differ = CustomDiffer(U=False)

    a = [0.001, 0.01, 0.1]
    b = [0.002, 0.02, 0.2]

    assert {'D': [{'I': 2, 'N': 0.2, 'O': 0.1}]} == differ.diff(a, b)
