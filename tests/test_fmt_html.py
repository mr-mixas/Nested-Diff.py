import pytest

from nested_diff.formatters import HtmlFormatter

import tests.data.formatters
import tests.data.formatters.HtmlFormatter

from tests.common import do_test_function, iterate_test_suite


def function_to_test(test):
    formatter = HtmlFormatter(**test.get('formatter_opts', {}))

    return formatter.format(test['diff'], **test.get('format_func_opts', {}))


@pytest.mark.parametrize(
    ('test', 'func'),
    iterate_test_suite(
        tests.data.formatters.get_tests(),
        tests.data.formatters.HtmlFormatter,
        function_to_test,
    ),
)
def test_all(test, func):
    do_test_function(test, func)
