# Nested-Diff.py

Recursive diff and patch for nested structures. **[Live Demo](https://nesteddiff.pythonanywhere.com/)**

[![Tests Status](https://github.com/mr-mixas/Nested-Diff.py/actions/workflows/tests.yml/badge.svg)](https://github.com/mr-mixas/Nested-Diff.py/actions?query=branch%3Amaster)
[![Coverage Status](https://coveralls.io/repos/github/mr-mixas/Nested-Diff.py/badge.svg)](https://coveralls.io/github/mr-mixas/Nested-Diff.py)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/nested_diff.svg)](https://pypi.org/project/nested_diff/)
[![License](https://img.shields.io/pypi/l/nested_diff.svg)](https://pypi.org/project/nested_diff/)

## Install

`pip install nested_diff`

For extra formats support (YAML, TOML) in cli tools, use

`pip install nested_diff[cli]`

## Command line tools

```
mixas:~/$ cat a.json b.json
[0, [1],    3]
[0, [1, 2], 3]
mixas:~/$ nested_diff a.json b.json
  [1]
+   [1]
+     2
mixas:~/$
mixas:~/$ nested_diff a.json b.json --ofmt json > patch.json
mixas:~/$ nested_patch a.json patch.json
```

## Library usage

```
>>> from nested_diff import diff, patch
>>>
>>> a = {'one': 1, 'two': 2, 'three': 3}
>>> b = {'one': 1, 'two': 42}
>>>
>>> diff(a, b)
{'D': {'three': {'R': 3}, 'two': {'N': 42, 'O': 2}, 'one': {'U': 1}}}
>>>
>>> diff(a, b, O=False, U=False)
{'D': {'three': {'R': 3}, 'two': {'N': 42}}}
>>>
>>>
>>> c = [0,1,2,3]
>>> d = [  1,2,4,5]
>>>
>>> c = patch(c, diff(c, d))
>>> assert c == d
>>>
```

### Formatting diffs

```
>>> from nested_diff import diff
>>> from nested_diff.fmt import TextFormatter
>>>
>>> a = {'one': 1, 'two': 'some\ntext\ninside'}
>>> b = {'one': 0, 'two': 'some\ntext'}
>>>
>>> d = diff(a, b, U=False, text_diff_ctx=3)
>>> print(TextFormatter().format(d))
  {'one'}
-   1
+   0
  {'two'}
#   <str>
    @@ -1,3 +1,2 @@
    some
    text
-   inside
<BLANKLINE>
>>>
```

See more examples in [HOWTO](./HOWTO.md) and [tests](./tests/).

## Diff structure

Diff is a dict and may contain status keys:

* `A` stands for 'added', it's value - added item.
* `D` means 'different' and contains subdiff.
* `N` is a new value for changed item.
* `O` is a changed item's old value.
* `R` key used for removed item.
* `U` represent unchanged item.

and auxiliary keys:

* `C` comment; optional, value - arbitrary string.
* `E` diffed entity (optional), value - empty instance of entity's class.
* `I` index for sequence item, used only when prior item was omitted.

Diff metadata alternates with actual data; simple types specified as is, dicts,
lists and tuples contain subdiffs for their items with native for such types
addressing: indexes for lists and tuples, keys for dictionaries. Any status
key, except `D` may be omitted during diff computation. `E` key is used with
`D` when entity unable to contain diff by itself (set, frozenset for example);
`D` contain a list of subdiffs in this case.

### Annotated example:

```
a:  {"one": [5,7]}
b:  {"one": [5], "two": 2}
opts: U=False  # omit unchanged items

diff:
{"D": {"one": {"D": [{"I": 1, "R": 7}]}, "two": {"A": 2}}}
| |   |  |    | |   || |   |   |   |       |    | |   |
| |   |  |    | |   || |   |   |   |       |    | |   +- with value 2
| |   |  |    | |   || |   |   |   |       |    | +- key 'two' was added
| |   |  |    | |   || |   |   |   |       |    +- subdiff for it
| |   |  |    | |   || |   |   |   |       +- another key from top-level
| |   |  |    | |   || |   |   |   +- what it was (item's value: 7)
| |   |  |    | |   || |   |   +- what happened to item (removed)
| |   |  |    | |   || |   +- list item's actual index
| |   |  |    | |   || +- prior item was omitted
| |   |  |    | |   |+- subdiff for list item
| |   |  |    | |   +- it's value - list
| |   |  |    | +- it is deeply changed
| |   |  |    +- subdiff for key 'one'
| |   |  +- it has key 'one'
| |   +- top-level thing is a dict
| +- changes somewhere deeply inside
+- diff is always a dict
```

## License

Licensed under the terms of the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

## See Also

[HOWTO](./HOWTO.md)

[deepdiff](https://pypi.org/project/deepdiff/),
[jsondiff](https://pypi.org/project/jsondiff/),
[jsonpatch](https://pypi.org/project/jsonpatch/),
[json-delta](https://pypi.org/project/json-delta/)
