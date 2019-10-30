import pytest
import sys

from nested_diff import cli


class Dumper(cli.Dumper):
    def encode(self, data):
        return data


def test_dumper_dump_default_with_tty(stringio_tty):
    dumper = Dumper()
    dumper.dump(stringio_tty, 'text')

    assert 'text' == stringio_tty.getvalue()


def test_dumper_dump_default_without_tty(stringio):
    dumper = Dumper()
    dumper.dump(stringio, 'text')

    assert 'text' == stringio.getvalue()


def test_dumper_dump_final_new_line_with_tty(stringio_tty):
    dumper = Dumper()
    dumper.tty_final_new_line = True
    dumper.dump(stringio_tty, 'text')

    assert 'text\n' == stringio_tty.getvalue()


def test_dumper_dump_final_new_line_without_tty(stringio):
    dumper = Dumper()
    dumper.tty_final_new_line = True
    dumper.dump(stringio, 'text')

    assert 'text' == stringio.getvalue()


def test_exit_code_wrong_args(fullname):
    with pytest.raises(SystemExit) as e:
        cli.App(args=('--unsupported-option')).run()

    assert e.value.code == 2


def test_excepthook_overrided():
    orig_id = id(sys.excepthook)
    cli.App(args=())

    assert orig_id != id(sys.excepthook)


def test_excepthook_raise_system_exit_127():
    sys.excepthook = sys.__excepthook__  # restore (changed by prev tests)
    cli.App(args=())  # should set sys.excepthook which raises SystemExit(127)

    with pytest.raises(SystemExit) as e:
        sys.excepthook(None, None, None)

    assert e.value.code == 127


def test_guess_fmt_aliases():
    class FakeFP(object):
        name = None

    aliases = {
        'yml': 'yaml',
    }
    fake_fp = FakeFP()
    app = cli.App(args=())

    for ext in sorted(aliases):
        fake_fp.name = 'filename.' + ext
        assert aliases[ext] == app.guess_fmt(fake_fp, 'default')


def test_guess_fmt_ignore_fp_defaults():
    app = cli.App(args=())
    for fp in sys.stdin, sys.stdout, sys.stderr:
        assert 'default' == app.guess_fmt(fp, 'default')


def test_get_loader_unsupported_fmt():
    app = cli.App(args=())

    with pytest.raises(RuntimeError, match='Unsupported input format: garbage'):
        app.get_loader('garbage')
