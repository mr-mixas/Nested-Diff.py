import io
import json
import pytest

from unittest import mock
from shutil import copyfile

import nested_diff.patch_tool


def test_default_patch(capsys, content, fullname, tmp_path):
    result_file_name = '{}.got.json'.format(tmp_path)
    copyfile(
        fullname('lists.a.json', shared=True),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        fullname('lists.patch.yaml', shared=True),
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err
    assert exit_code == 0

    assert json.loads(content(fullname('lists.b.json', shared=True))) == \
        json.loads(content(result_file_name))


def test_json_ofmt_opts(capsys, content, expected, fullname, tmp_path):
    result_file_name = '{}.got.json'.format(tmp_path)
    copyfile(
        fullname('lists.a.json', shared=True),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        fullname('lists.patch.json', shared=True),
        '--ofmt', 'json',
        '--ofmt-opts', '{"indent": null}',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err
    assert exit_code == 0

    assert json.loads(expected) == json.loads(content(result_file_name))


def test_auto_fmts(capsys, content, expected, fullname, tmp_path):
    result_file_name = '{}.got.yaml'.format(tmp_path)
    copyfile(
        fullname('lists.a.yaml', shared=True),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        fullname('lists.patch.json', shared=True),
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err
    assert exit_code == 0

    assert expected == content(result_file_name)


def test_yaml_ifmt(capsys, content, fullname, tmp_path):
    result_file_name = '{}.got'.format(tmp_path)
    copyfile(
        fullname('lists.a.yaml', shared=True),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        fullname('lists.patch.yaml', shared=True),
        '--ifmt', 'yaml',
        '--ofmt', 'json',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err
    assert exit_code == 0

    # output is json by default
    assert json.loads(content(fullname('lists.b.json', shared=True))) == \
        json.loads(content(result_file_name))


def test_yaml_ofmt(capsys, content, expected, fullname, tmp_path):
    result_file_name = '{}.got.json'.format(tmp_path)
    copyfile(
        fullname('lists.a.json', shared=True),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        fullname('lists.patch.json', shared=True),
        '--ofmt', 'yaml',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err
    assert exit_code == 0

    assert expected == content(result_file_name)


def test_ini_ofmt(capsys, content, fullname, tmp_path):
    result_file_name = '{}.got.ini'.format(tmp_path)
    copyfile(
        fullname('a.ini', shared=True),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        fullname('ini.patch.json', shared=True),
        '--ofmt', 'ini',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err
    assert exit_code == 0

    expected = content(fullname('b.ini', shared=True))
    assert expected == content(result_file_name)


def test_toml_fmt(capsys, content, fullname, tmp_path):
    result_file_name = '{}.got.toml'.format(tmp_path)
    copyfile(
        fullname('dict.a.toml', shared=True),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        fullname('dict.patch.toml', shared=True),
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err
    assert exit_code == 0

    expected = content(fullname('dict.b.toml', shared=True))
    assert expected == content(result_file_name)


def test_entry_point(capsys):
    with mock.patch('sys.argv', ['nested_patch', '-h']):
        with pytest.raises(SystemExit) as e:
            nested_diff.patch_tool.cli()

        assert e.value.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith('usage: nested_patch')
    assert '' == captured.err


def test_stdin_patch(capsys, content, fullname, tmp_path):
    result_file_name = '{}.got.json'.format(tmp_path)
    copyfile(
        fullname('lists.a.json', shared=True),
        result_file_name,
    )

    patch = io.StringIO(content(fullname('lists.patch.json', shared=True)))

    with mock.patch('sys.stdin', patch):
        exit_code = nested_diff.patch_tool.App(
            args=(result_file_name, '--ifmt', 'json')).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err
    assert exit_code == 0

    assert json.loads(content(fullname('lists.b.json', shared=True))) == \
        json.loads(content(result_file_name))


def test_arg_files_absent():
    with pytest.raises(SystemExit) as e:
        nested_diff.patch_tool.App(args=('/file/not/exists')).run()

    assert e.value.code == 2
