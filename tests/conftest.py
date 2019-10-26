import os
import pytest

from io import StringIO


def get_testfile_name(request, suffix='dat', shared=False):
    if shared:
        return os.path.join(
            os.path.dirname(request.module.__file__),
            'shared.' + suffix
        )
    else:
        return os.path.splitext(request.module.__file__)[0] + \
            '.' + request.function.__name__ + '.' + suffix


@pytest.fixture
def content():
    def _reader(filename):
        with open(filename) as f:
            return f.read()

    return _reader


@pytest.fixture
def expected(request):
    name = get_testfile_name(request, suffix='exp')
    with open(name) as f:
        return f.read()


@pytest.fixture
def fullname(request):
    def _name_getter(suffix, shared=False):
        return get_testfile_name(request, suffix=suffix, shared=shared)

    return _name_getter


@pytest.fixture
def testfile(request):
    def _content_getter(suffix, shared=False):
        filename = get_testfile_name(request, suffix=suffix, shared=shared)
        with open(filename) as f:
            return f.read()

    return _content_getter


@pytest.fixture
def stringio():
    return StringIO()


class _StringIOTTY(StringIO):
    def isatty(self):
        return True


@pytest.fixture
def stringio_tty():
    return _StringIOTTY()
