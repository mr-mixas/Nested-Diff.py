import json
import pytest
import sys

from unittest import mock

import nested_diff.diff_tool


def test_default_diff(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.yaml', shared=True),
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_default_diff_with_tty(capsys, expected, fullname, stringio_tty):
    with mock.patch('sys.stdout.isatty', return_value=True):
        exit_code = nested_diff.diff_tool.App(args=(
            fullname('lists.a.json', shared=True),
            fullname('lists.b.json', shared=True),
        )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_diff_method_kwargs_override(capsys, expected, fullname):
    class TestApp(nested_diff.diff_tool.App):
        def diff(self, a, b, **kwargs):
            return super().diff(a, b, A=0, U=1)

    exit_code = TestApp(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.yaml', shared=True),
        '-A', '1',
        '-U', '0',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_enable_U_ops(capsys, expected, fullname):  # noqa N802
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'json',
        '-U=1', '-U', '1',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_trimR_ops(capsys, expected, fullname):  # noqa N802
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.b.json', shared=True),
        fullname('lists.a.json', shared=True),
        '-R=trim', '-R', 'trim',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_output_file(capsys, content, expected, fullname, tmp_path):
    result_file_name = '{}.got'.format(tmp_path)
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'json',
        '--out', result_file_name,
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert '' == captured.out
    assert exit_code == 1

    assert json.loads(expected) == json.loads(content(result_file_name))


def test_json_ofmt_opts(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'json',
        '--ofmt-opts', '{"indent": null}',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_ini_ifmt(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('a.ini', shared=True),
        fullname('b.ini', shared=True),
        '--ifmt', 'ini',
        '--ofmt', 'json',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_text_default(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('text.a.json', shared=True),
        fullname('text.b.json', shared=True),
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_text_default_term(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('text.a.json', shared=True),
        fullname('text.b.json', shared=True),
        '--ofmt', 'term',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_text_context_0(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('text.a.json', shared=True),
        fullname('text.b.json', shared=True),
        '--text-ctx', '0',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_text_disabled(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('text.a.json', shared=True),
        fullname('text.b.json', shared=True),
        '--text-ctx', '-1',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_html_ofmt(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'html',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


@pytest.mark.skipif(
    sys.platform == 'win32',
    reason='win use non utf-8 encoding by default, we have utf-8 only sample',
)
def test_html_ofmt_opts(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'html',
        '--ofmt-opts', '{"html_opts": {"lang": "es", "title": "<título>"}}',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_html_ofmt_wrappings(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'html',
        '--ofmt-opts', '{"html_opts": {"header": "<html>", "footer": "</html>", "title": "ignored"}}',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_text_ofmt(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'text',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_term_ofmt(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'term',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


@pytest.mark.skipif(sys.version_info < (3, 6), reason='different keys order')
def test_toml_fmt(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('dict.a.toml', shared=True),
        fullname('dict.b.toml', shared=True),
        '--ofmt', 'toml',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_yaml_ifmt(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.yaml', shared=True),
        fullname('lists.b.yaml', shared=True),
        '--ifmt', 'yaml',
        '--ofmt', 'json',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_yaml_ofmt(capsys, expected, fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'yaml',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert exit_code == 1

    assert expected == captured.out


def test_exit_code_diff_absent(fullname):
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.a.json', shared=True),
    )).run()

    assert exit_code == 0


def test_exit_code_diff_absent_U_opt_enabled(fullname):  # noqa N802
    exit_code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.a.json', shared=True),
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
    assert '' == captured.err
