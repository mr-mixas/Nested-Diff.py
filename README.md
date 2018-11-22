# {Nested: Diff}.py

Recursive diff for nested structures, implementation of [Nested-Diff](https://github.com/mr-mixas/Nested-Diff)

[![Build Status](https://travis-ci.org/mr-mixas/Nested-Diff.py.svg?branch=master)](https://travis-ci.org/mr-mixas/Nested-Diff.py)
[![Coverage Status](https://coveralls.io/repos/github/mr-mixas/Nested-Diff.py/badge.svg?branch=master)](https://coveralls.io/github/mr-mixas/Nested-Diff.py?branch=master)

## Status

Alpha, WIP.

## Usage

```
>>> from nested_diff import diff
>>>
>>> a = {'one': 1, 'two': 2, 'three': 3}
>>> b = {'one': 1, 'two': 42}
>>> diff(a, b)
{'D': {'three': {'R': 3}, 'two': {'O': 2, 'N': 42}, 'one': {'U': 1}}}
>>>
>>> diff(a, b, O=False, R=False)
{'D': {'two': {'N': 42}, 'one': {'U': 1}}}
>>>
```

## License

Licensed under the terms of the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0>).
