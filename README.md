# Nested-Diff.py

Recursive diff for python nested structures, implementation of
[Nested-Diff](https://github.com/mr-mixas/Nested-Diff)

Builtin containers traversed recursively, all other types compared by values.

[![Build Status](https://travis-ci.org/mr-mixas/Nested-Diff.py.svg?branch=master)](https://travis-ci.org/mr-mixas/Nested-Diff.py)
[![Coverage Status](https://coveralls.io/repos/github/mr-mixas/Nested-Diff.py/badge.svg)](https://coveralls.io/github/mr-mixas/Nested-Diff.py)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/nested_diff.svg)](https://pypi.org/project/nested_diff/)
[![License](https://img.shields.io/pypi/l/nested_diff.svg)](https://pypi.org/project/nested_diff/)

## Diff format

Diff is a dict and may contain following keys:

* `A` stands for 'added', it's value - added item.
* `D` means 'different' and contains subdiff.
* `I` index for sequence item, used only when prior item was omitted.
* `N` is a new value for changed item.
* `O` is a changed item's old value.
* `R` key used for removed item.
* `U` represent unchanged item.

Diff metadata alternates with actual data; simple types specified as is, dicts,
lists, sets and tuples contain subdiffs for their items with native for such
types addressing: indexes for lists and tuples and keys for dictionaries. Each
status type, except `D` and `I`, may be omitted during diff computation.

Annotated example:

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

## Examples

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
>>> diff(c, d, O=False, U=False)
{'D': [{'R': 0}, {'I': 3, 'N': 4}, {'A': 5}]}
>>>
>>>
>>> c = patch(c, diff(c, d))
>>> assert c == d
>>>
>>>
>>> a = {   1, 2, 4, 5}
>>> b = {0, 1, 2, 3}
>>>
>>> Differ(U=False).diff_sets(a, b)
{'D': {{'A': 0}, {'R': 4}, {'A': 3}, {'R': 5}}}
>>>
```

## Subclassing

```
from nested_diff import Differ

class CustomDiffer(Differ):
    """
    Diff floats using defined precision
    """
    def diff__default(self, a, b):
        if isinstance(a, float) and isinstance(a, type(b)):
            if round(a, 1) == round(b, 1):
                return {'U': a} if self.op_u else {}

        return super(CustomDiffer, self).diff__default(a, b)


differ = CustomDiffer(U=False)

a = [0.001, 0.01, 0.1]
b = [0.002, 0.02, 0.2]

assert {'D': [{'I': 2, 'N': 0.2, 'O': 0.1}]} == differ.diff(a, b)
```

## License

Licensed under the terms of the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0>).

## See Also

[deepdiff](https://pypi.org/project/deepdiff/),
[jsonpatch](https://pypi.org/project/jsonpatch/),
[json-delta](https://pypi.org/project/json-delta/)
