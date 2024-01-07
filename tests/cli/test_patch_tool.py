import io
import json
import pytest

from unittest import mock
from shutil import copyfile

import nested_diff.patch_tool


def test_default_patch(capsys, content, rpath, tmp_path):
    result_file_name = '{}.got.json'.format(tmp_path)
    copyfile(
        rpath('shared.lists.a.json'),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        rpath('shared.lists.patch.yaml'),
    )).run()

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    assert exit_code == 0

    expected = json.loads(content(rpath('shared.lists.b.json')))
    assert json.loads(content(result_file_name)) == expected


def test_json_ofmt_opts(capsys, content, expected, rpath, tmp_path):
    result_file_name = '{}.got.json'.format(tmp_path)
    copyfile(
        rpath('shared.lists.a.json'),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        rpath('shared.lists.patch.json'),
        '--ofmt', 'json',
        '--ofmt-opts', '{"indent": null}',
    )).run()

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    assert exit_code == 0

    assert json.loads(content(result_file_name)) == json.loads(expected)


def test_auto_fmts(capsys, content, expected, rpath, tmp_path):
    result_file_name = '{}.got.yaml'.format(tmp_path)
    copyfile(
        rpath('shared.lists.a.yaml'),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        rpath('shared.lists.patch.json'),
    )).run()

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    assert exit_code == 0

    assert content(result_file_name) == expected


def test_yaml_ifmt(capsys, content, rpath, tmp_path):
    result_file_name = '{}.got'.format(tmp_path)
    copyfile(
        rpath('shared.lists.a.yaml'),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        rpath('shared.lists.patch.yaml'),
        '--ifmt', 'yaml',
        '--ofmt', 'json',
    )).run()

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    assert exit_code == 0

    # output is json by default
    expected = json.loads(content(rpath('shared.lists.b.json')))
    assert json.loads(content(result_file_name)) == expected


def test_yaml_ofmt(capsys, content, expected, rpath, tmp_path):
    result_file_name = '{}.got.json'.format(tmp_path)
    copyfile(
        rpath('shared.lists.a.json'),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        rpath('shared.lists.patch.json'),
        '--ofmt', 'yaml',
    )).run()

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    assert exit_code == 0

    assert content(result_file_name) == expected


def test_ini_ofmt(capsys, content, rpath, tmp_path):
    result_file_name = '{}.got.ini'.format(tmp_path)
    copyfile(
        rpath('shared.a.ini'),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        rpath('shared.ini.patch.json'),
        '--ofmt', 'ini',
    )).run()

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    assert exit_code == 0

    expected = content(rpath('shared.b.ini'))
    assert content(result_file_name) == expected


def test_toml_fmt(capsys, content, rpath, tmp_path):
    result_file_name = '{}.got.toml'.format(tmp_path)
    copyfile(
        rpath('shared.dict.a.toml'),
        result_file_name,
    )
    exit_code = nested_diff.patch_tool.App(args=(
        result_file_name,
        rpath('shared.dict.patch.toml'),
    )).run()

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    assert exit_code == 0

    expected = content(rpath('shared.dict.b.toml'))
    assert content(result_file_name) == expected


def test_entry_point(capsys):
    with mock.patch('sys.argv', ['nested_patch', '-h']):
        with pytest.raises(SystemExit) as e:
            nested_diff.patch_tool.App.cli()

        assert e.value.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith('usage: nested_patch')
    assert captured.err == ''


def test_stdin_patch(capsys, content, rpath, tmp_path):
    result_file_name = '{}.got.json'.format(tmp_path)
    copyfile(
        rpath('shared.lists.a.json'),
        result_file_name,
    )

    patch = io.StringIO(content(rpath('shared.lists.patch.json')))

    with mock.patch('sys.stdin', patch):
        exit_code = nested_diff.patch_tool.App(
            args=(result_file_name, '--ifmt', 'json')).run()

    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == ''
    assert exit_code == 0

    expected = json.loads(content(rpath('shared.lists.b.json')))
    assert json.loads(content(result_file_name)) == expected


def test_arg_files_absent():
    with pytest.raises(SystemExit) as e:
        nested_diff.patch_tool.App(args=('/file/not/exists')).run()

    assert e.value.code == 2
