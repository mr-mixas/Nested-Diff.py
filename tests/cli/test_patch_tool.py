import json
import pytest

from unittest import mock
from shutil import copyfile

import nested_diff.patch_tool


def test_default_patch(capsys, content, fullname):
    copyfile(
        fullname('lists.a.json', shared=True),
        fullname('got'),
    )
    nested_diff.patch_tool.App(args=(
        fullname('got'),
        fullname('lists.patch.json', shared=True),
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err

    assert json.loads(content(fullname('lists.b.json', shared=True))) == \
        json.loads(content(fullname('got')))


def test_json_ofmt_opts(capsys, content, expected, fullname):
    copyfile(
        fullname('lists.a.json', shared=True),
        fullname('got'),
    )
    nested_diff.patch_tool.App(args=(
        fullname('got'),
        fullname('lists.patch.json', shared=True),
        '--ofmt', 'json',
        '--ofmt-opts', '{"indent": null}',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err

    assert json.loads(expected) == json.loads(content(fullname('got')))


def test_yaml_ifmt(capsys, content, fullname):
    copyfile(
        fullname('lists.a.yaml', shared=True),
        fullname('got'),
    )
    nested_diff.patch_tool.App(args=(
        fullname('got'),
        fullname('lists.patch.yaml', shared=True),
        '--ifmt', 'yaml',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err

    # output is json by default
    assert json.loads(content(fullname('lists.b.json', shared=True))) == \
        json.loads(content(fullname('got')))


def test_yaml_ofmt(capsys, content, expected, fullname):
    copyfile(
        fullname('lists.a.json', shared=True),
        fullname('got'),
    )
    nested_diff.patch_tool.App(args=(
        fullname('got'),
        fullname('lists.patch.json', shared=True),
        '--ofmt', 'yaml',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err

    assert expected == content(fullname('got'))


def test_entry_point(capsys):
    with mock.patch('sys.argv', ['nested_patch', '-h']):
        with pytest.raises(SystemExit) as e:
            nested_diff.patch_tool.cli()

        assert e.value.code == 0

    captured = capsys.readouterr()
    assert captured.out.startswith('usage: nested_patch [-h] [--version]')
    assert '' == captured.err
