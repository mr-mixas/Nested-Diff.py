import sys

import pytest

from nested_diff import cli


class Dumper(cli.Dumper):
    def encode(self, data):
        return data


def test_base_dumper_encode():
    assert cli.Dumper().encode('data') == 'data'


def test_base_loader_decode():
    assert cli.Loader().decode('data') == 'data'


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


def test_guess_fmt():
    class FakeFP:
        name = None

    exts = {
        'ini': 'ini',
        'json': 'json',
        'py': 'default',
        'txt': 'default',
        'yml': 'yaml',
    }
    fake_fp = FakeFP()

    for ext, fmt in sorted(exts.items()):
        fake_fp.name = f'filename.{ext}'
        assert cli.App(args=()).guess_fmt(fake_fp, 'default') == fmt


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


def test_loader_yaml_custom_tags():
    loaded = cli.YamlLoader().decode('!custom_tag')

    assert isinstance(loaded, cli.YamlNode)
    assert loaded.tag == '!custom_tag'
    assert loaded.value == ''


def test_run():
    with pytest.raises(NotImplementedError):
        cli.App(args=()).run()
