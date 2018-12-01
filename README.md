# Nested-Diff.py

Recursive diff for nested structures, implementation of [Nested-Diff](https://github.com/mr-mixas/Nested-Diff)

Dicts and lists traversed recursively, all other types compared by values.

[![Build Status](https://travis-ci.org/mr-mixas/Nested-Diff.py.svg?branch=master)](https://travis-ci.org/mr-mixas/Nested-Diff.py)
[![Coverage Status](https://coveralls.io/repos/github/mr-mixas/Nested-Diff.py/badge.svg)](https://coveralls.io/github/mr-mixas/Nested-Diff.py)

## Status

Alpha, WIP.

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
```

## License

Licensed under the terms of the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0>).

## See Also

[deepdiff](https://pypi.org/project/deepdiff/),
[jsonpatch](https://pypi.org/project/jsonpatch/),
[json-delta](https://pypi.org/project/json-delta/)
