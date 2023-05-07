import json
import pytest
import sys

from unittest import mock

import nested_diff.diff_tool


def test_default_diff(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.yaml'),
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_default_diff_with_tty(capsys, expected, rpath, stringio_tty):
    with mock.patch('sys.stdout.isatty', return_value=True):
        exit_code = nested_diff.diff_tool.App(args=(
            rpath('shared.lists.a.json'),
            rpath('shared.lists.b.json'),
        )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_diff_method_kwargs_override(capsys, expected, rpath):
    class TestApp(nested_diff.diff_tool.App):
        def diff(self, a, b, **kwargs):
            return super().diff(a, b, A=0, U=1)

    exit_code = TestApp(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.yaml'),
        '-A', '1',
        '-U', '0',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_enable_U_ops(capsys, expected, rpath):  # noqa N802
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        '--ofmt', 'json',
        '-U=1', '-U', '1',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_trimR_ops(capsys, expected, rpath):  # noqa N802
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.b.json'),
        rpath('shared.lists.a.json'),
        '-R=trim', '-R', 'trim',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_output_file(capsys, content, expected, rpath, tmp_path):
    result_file_name = '{}.got'.format(tmp_path)
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        '--ofmt', 'json',
        '--out', result_file_name,
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out == ''
    assert exit_code == 1

    assert json.loads(content(result_file_name)) == json.loads(expected)


def test_json_ofmt_opts(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        '--ofmt', 'json',
        '--ofmt-opts', '{"indent": null}',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_ini_ifmt(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.a.ini'),
        rpath('shared.b.ini'),
        '--ifmt', 'ini',
        '--ofmt', 'json',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_text_default(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.text.a.json'),
        rpath('shared.text.b.json'),
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_text_default_term(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.text.a.json'),
        rpath('shared.text.b.json'),
        '--ofmt', 'term',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_text_context_0(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.text.a.json'),
        rpath('shared.text.b.json'),
        '--text-ctx', '0',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_text_disabled(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.text.a.json'),
        rpath('shared.text.b.json'),
        '--text-ctx', '-1',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_html_ofmt(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        '--ofmt', 'html',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


@pytest.mark.skipif(
    sys.platform == 'win32',
    reason='win use non utf-8 encoding by default, we have utf-8 only sample',
)
def test_html_ofmt_opts(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        '--ofmt', 'html',
        '--ofmt-opts', '{"lang": "es", "title": "<título>"}',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_html_ofmt_wrappings(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        '--ofmt', 'html',
        '--ofmt-opts', '{"header": "<html>", "footer": "</html>", "title": "ignored"}',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_text_ofmt(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        '--ofmt', 'text',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_term_ofmt(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        '--ofmt', 'term',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


@pytest.mark.skipif(sys.version_info < (3, 6), reason='different keys order')
def test_toml_fmt(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.dict.a.toml'),
        rpath('shared.dict.b.toml'),
        '--ofmt', 'toml',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_yaml_ifmt(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.yaml'),
        rpath('shared.lists.b.yaml'),
        '--ifmt', 'yaml',
        '--ofmt', 'json',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_yaml_ofmt(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        '--ofmt', 'yaml',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


# json parser return same NaN object for all NaN entries (at least for now),
# so they all match `a is b` condition in Differ.diff and treated as equal.
def test_json_nan(capsys, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.nan.json'),
        rpath('shared.nan.json'),
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out == ''
    assert exit_code == 0


# yaml parser return same NaN object for all NaN entries (at least for now),
# so they all match `a is b` condition in Differ.diff and treated as equal.
def test_yaml_nan(capsys, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.nan.yaml'),
        rpath('shared.nan.yaml'),
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert captured.out == ''
    assert exit_code == 0


def test_quiet_diff(capsys, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.yaml'),
        '--quiet',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == ''


def test_exit_code_diff_absent(rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.a.json'),
    )).run()

    assert exit_code == 0


def test_exit_code_diff_absent_U_opt_enabled(rpath):  # noqa N802
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.a.json'),
        '-U=1',
    )).run()

    assert exit_code == 0


def test_entry_point(capsys):
    with mock.patch('sys.argv', ['nested_diff', '-h']):
        with pytest.raises(SystemExit) as e:
            nested_diff.diff_tool.cli()

        assert e.value.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith('usage: nested_diff')
    assert captured.err == ''


def test_diff_single_arg(capsys, rpath):
    with pytest.raises(SystemExit) as e:
        nested_diff.diff_tool.App(args=[rpath('shared.lists.a.json')]).run()

    assert e.value.code == 2


def test_diff_several_args(capsys, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        rpath('shared.lists.a.json'),
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    # can't use expected file here because of path sep on windows
    assert captured.out.startswith('--- tests')


def test_diff_several_args_tty(capsys, rpath, stringio_tty):
    app = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        rpath('shared.lists.a.json'),
    ))
    app.args.out = stringio_tty
    exit_code = app.run()

    assert capsys.readouterr().err == ''
    assert exit_code == 1

    assert stringio_tty.getvalue().startswith('\033[33m--- tests')


def test_diff_several_args_html(capsys, rpath, stringio_tty):
    app = nested_diff.diff_tool.App(args=(
        rpath('shared.lists.a.json'),
        rpath('shared.lists.b.json'),
        rpath('shared.lists.a.json'),
        '--ofmt', 'html',
    ))
    app.args.out = stringio_tty
    exit_code = app.run()

    assert capsys.readouterr().err == ''
    assert exit_code == 1

    assert stringio_tty.getvalue().count('</html>') == 1


def test_show_single_arg(capsys, expected, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.ini.patch.json'),
        '--show',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out == expected


def test_show_several_args(capsys, rpath):
    exit_code = nested_diff.diff_tool.App(args=(
        rpath('shared.ini.patch.json'),
        rpath('shared.ini.patch.json'),
        '--show',
    )).run()

    captured = capsys.readouterr()
    assert captured.err == ''
    assert exit_code == 1

    assert captured.out.startswith('--- /dev/null')


def test_show_several_args_tty(capsys, rpath, stringio_tty):
    app = nested_diff.diff_tool.App(args=(
        rpath('shared.ini.patch.json'),
        rpath('shared.ini.patch.json'),
        '--show',
    ))
    app.args.out = stringio_tty
    exit_code = app.run()

    assert capsys.readouterr().err == ''
    assert exit_code == 1

    assert stringio_tty.getvalue().startswith('\033[33m--- /dev/null')
