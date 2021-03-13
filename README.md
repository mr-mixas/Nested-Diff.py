# Nested-Diff.py

Recursive diff and patch for nested structures

[![Build Status](https://travis-ci.org/mr-mixas/Nested-Diff.py.svg?branch=master)](https://travis-ci.org/mr-mixas/Nested-Diff.py)
[![Coverage Status](https://coveralls.io/repos/github/mr-mixas/Nested-Diff.py/badge.svg)](https://coveralls.io/github/mr-mixas/Nested-Diff.py)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/nested_diff.svg)](https://pypi.org/project/nested_diff/)
[![License](https://img.shields.io/pypi/l/nested_diff.svg)](https://pypi.org/project/nested_diff/)

## Install

`pip install nested_diff`

## Command line tools examples

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

## Library usage examples

```
>>> from nested_diff import diff, patch
>>>
>>> a = {'one': 1, 'two': 2, 'three': 3}
>>> b = {'one': 1, 'two': 42}
>>>
>>> diff(a, b)
{'D': {'three': {'R': 3}, 'two': {'O': 2, 'N': 42}, 'one': {'U': 1}}}
>>>
>>> diff(a, b, O=False, U=False)
{'D': {'two': {'N': 42}, 'three': {'R': 3}}}
>>>
>>>
>>> c = [0,1,2,3]
>>> d = [  1,2,4,5]
>>>
>>> c = patch(c, diff(c, d))
>>> assert c == d
```

### Subclassing

```
from nested_diff import Differ


class CustomDiffer(Differ):
    """
    Use custom precision for floats.

    """
    def __init__(self, float_precision=2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_differ(float, self.diff_float)
        self.float_precision = float_precision

    def diff_float(self, a, b):
        if round(a, self.float_precision) == round(b, self.float_precision):
            return {'U': a} if self.op_u else {}

        return super().diff__default(a, b)


differ = CustomDiffer(float_precision=1, U=False)

a = [0.001, 0.01, 0.1]
b = [0.002, 0.02, 0.2]

assert {'D': [{'I': 2, 'N': 0.2, 'O': 0.1}]} == differ.diff(a, b)
```

### Formatting diffs

```
>>> from nested_diff import diff
>>> from nested_diff.fmt import TextFormatter
>>>
>>> a = {'one': 1, 'two': 'some\ntext\ninside'}
>>> b = {'one': 0, 'two': 'some\ntext'}
>>>
>>> d = diff(a, b, U=False, multiline_diff_context=3)
>>> print(TextFormatter().format(d))
  {'two'}
    @@ -1,3 +1,2 @@
    some
    text
-   inside
  {'one'}
-   1
+   0
>>>
```

## Diff format

Diff is a dict and may contain following keys:

* `A` stands for 'added', it's value - added item.
* `D` means 'different' and contains subdiff.
* `E` diffed entity (optional), value - empty instance of entity's class.
* `I` index for sequence item, used only when prior item was omitted.
* `N` is a new value for changed item.
* `O` is a changed item's old value.
* `R` key used for removed item.
* `U` represent unchanged item.

Diff metadata alternates with actual data; simple types specified as is, dicts,
lists and tuples contain subdiffs for their items with native for such types
addressing: indexes for lists and tuples and keys for dictionaries. Each status
type, except `D`. `E` and `I`, may be omitted during diff computation. `E` tag
is used with `D` when entity unable to contain diff by itself (set, frozenset);
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

[deepdiff](https://pypi.org/project/deepdiff/),
[jsondiff](https://pypi.org/project/jsondiff/),
[jsonpatch](https://pypi.org/project/jsonpatch/),
[json-delta](https://pypi.org/project/json-delta/)
