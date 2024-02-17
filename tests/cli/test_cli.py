import pytest
import sys

from nested_diff import cli


class Dumper(cli.Dumper):
    def encode(self, data):
        return data


def test_abstract_dumper_encode():
    with pytest.raises(NotImplementedError):
        cli.Dumper().encode('data')


def test_abstract_loader_decode():
    with pytest.raises(NotImplementedError):
        cli.Loader().decode('data')


def test_dumper_dump_default_with_tty(stringio_tty):
    dumper = Dumper()
    dumper.dump(stringio_tty, 'text')

    assert stringio_tty.getvalue() == 'text'


def test_dumper_dump_default_without_tty(stringio):
    dumper = Dumper()
    dumper.dump(stringio, 'text')

    assert stringio.getvalue() == 'text'


def test_dumper_dump_final_new_line_with_tty(stringio_tty):
    dumper = Dumper()
    dumper.tty_final_new_line = True
    dumper.dump(stringio_tty, 'text')

    assert stringio_tty.getvalue() == 'text\n'


def test_dumper_dump_final_new_line_without_tty(stringio):
    dumper = Dumper()
    dumper.tty_final_new_line = True
    dumper.dump(stringio, 'text')

    assert stringio.getvalue() == 'text'


def test_exit_code_wrong_args():
    with pytest.raises(SystemExit) as e:
        cli.App(args=('--unsupported-option')).run()

    assert e.value.code == 2


def test_excepthook_overridden():
    orig_id = id(sys.excepthook)
    cli.App(args=())

    assert id(sys.excepthook) != orig_id


def test_excepthook_raise_system_exit_127():
    sys.excepthook = sys.__excepthook__  # restore (changed by prev tests)
    cli.App(args=())  # should set sys.excepthook which raises SystemExit(127)

    with pytest.raises(SystemExit) as e:
        sys.excepthook(None, None, None)

    assert e.value.code == 127


def test_guess_fmt_aliases():
    class FakeFP:
        name = None

    aliases = {
        'yml': 'yaml',
    }
    fake_fp = FakeFP()

    for ext in sorted(aliases):
        fake_fp.name = f'filename.{ext}'
        assert cli.App(args=()).guess_fmt(fake_fp, 'default') == aliases[ext]


def test_guess_fmt_ignore_fp_defaults():
    for fp in sys.stdin, sys.stdout, sys.stderr:
        assert cli.App(args=()).guess_fmt(fp, 'default') == 'default'


def test_get_dumper_unsupported_fmt():
    with pytest.raises(
        RuntimeError,
        match='Unsupported output format: garbage',
    ):
        cli.App(args=()).get_dumper('garbage')


def test_get_loader_unsupported_fmt():
    with pytest.raises(
        RuntimeError,
        match='Unsupported input format: garbage',
    ):
        cli.App(args=()).get_loader('garbage')


def test_run():
    with pytest.raises(NotImplementedError):
        cli.App(args=()).run()
