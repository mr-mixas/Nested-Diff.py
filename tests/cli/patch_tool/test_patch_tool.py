import json
from shutil import copyfile

from nested_diff.patch_tool import App as PatchApp


def test_default_patch(capsys, content, fullname):
    copyfile(
        fullname('lists.a.json', shared=True),
        fullname('got'),
    )
    PatchApp(args=(
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
    PatchApp(args=(
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
    PatchApp(args=(
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
    PatchApp(args=(
        fullname('got'),
        fullname('lists.patch.json', shared=True),
        '--ofmt', 'yaml',
    )).run()

    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err

    assert expected == content(fullname('got'))
