import json
import pytest

from unittest import mock

import nested_diff.diff_tool


def test_default_diff(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.yaml', shared=True),
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err

    assert expected == captured.out


def test_default_diff_with_tty(capsys, expected, fullname, stringio_tty):
    with mock.patch('sys.stdout.isatty', return_value=True):
        nested_diff.diff_tool.App(args=(
            fullname('lists.a.json', shared=True),
            fullname('lists.b.json', shared=True),
        )).run()

    captured = capsys.readouterr()
    assert '' == captured.err

    assert expected == captured.out


def test_enable_U_ops(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'json',
        '-U=1', '-U', '1',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert expected == captured.out


def test_output_file(capsys, content, expected, fullname, tmp_path):
    result_file_name = '{}.got'.format(tmp_path)
    nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'json',
        '--out', result_file_name,
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert '' == captured.out

    assert json.loads(expected) == json.loads(content(result_file_name))


def test_json_ofmt_opts(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'json',
        '--ofmt-opts', '{"indent": null}',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert expected == captured.out


def test_ini_ifmt(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('a.ini', shared=True),
        fullname('b.ini', shared=True),
        '--ifmt', 'ini',
        '--ofmt', 'json',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert expected == captured.out


def test_multiline_default(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('multiline.a.json', shared=True),
        fullname('multiline.b.json', shared=True),
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert expected == captured.out


def test_multiline_default_term(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('multiline.a.json', shared=True),
        fullname('multiline.b.json', shared=True),
        '--ofmt', 'term',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert expected == captured.out


def test_multiline_context_0(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('multiline.a.json', shared=True),
        fullname('multiline.b.json', shared=True),
        '--text-ctx', '0',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert expected == captured.out


def test_multiline_disabled(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('multiline.a.json', shared=True),
        fullname('multiline.b.json', shared=True),
        '--text-ctx', '-1',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert expected == captured.out


def test_text_ofmt(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'text',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert expected == captured.out


def test_term_ofmt(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'term',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert expected == captured.out


def test_yaml_ifmt(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('lists.a.yaml', shared=True),
        fullname('lists.b.yaml', shared=True),
        '--ifmt', 'yaml',
        '--ofmt', 'json',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert expected == captured.out


def test_yaml_ofmt(capsys, expected, fullname):
    nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
        '--ofmt', 'yaml',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.err
    assert expected == captured.out


def test_exit_code_diff_absent(fullname):
    code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.a.json', shared=True),
    )).run()

    assert code == 0


def test_exit_code_diff_absent_U_opt_enabled(fullname):
    code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.a.json', shared=True),
        '-U=1',
    )).run()

    assert code == 0


def test_exit_code_diff_present(fullname):
    code = nested_diff.diff_tool.App(args=(
        fullname('lists.a.json', shared=True),
        fullname('lists.b.json', shared=True),
    )).run()

    assert code == 1


def test_entry_point(capsys):
    with mock.patch('sys.argv', ['nested_diff', '-h']):
        with pytest.raises(SystemExit) as e:
            nested_diff.diff_tool.cli()

        assert e.value.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith('usage: nested_diff')
    assert '' == captured.err
