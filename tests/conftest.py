import os
import pytest

from io import StringIO


pytest.register_assert_rewrite('tests.common')


@pytest.fixture()
def content():
    def _reader(filename):
        with open(filename) as f:
            return f.read()

    return _reader


@pytest.fixture()
def expected(request):
    filename = os.path.splitext(request.module.__file__)[0]
    filename += f'.{request.function.__name__}.exp'

    with open(filename) as f:
        return f.read()


@pytest.fixture()
def rpath(request):
    def _path_resolver(filename):
        path = os.path.join(
            os.path.dirname(request.module.__file__),
            filename,
        )

        return os.path.relpath(
            path,
            os.path.join(os.path.dirname(__file__), '..'),
        )

    return _path_resolver


@pytest.fixture()
def stringio():
    return StringIO()


class _StringIOTTY(StringIO):
    def isatty(self):
        return True


@pytest.fixture()
def stringio_tty():
    return _StringIOTTY()
