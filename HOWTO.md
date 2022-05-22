# Nested-Diff.py HowTo

## How to diff objects with types unsupported by nested\_diff

Custom type handlers may be set to support any desired types, have a look at
`Differ.set_handler` method and [handlers.py](nested_diff/handlers.py).

## How to ignore some differences during diff

Most obvious and simple way is to transform initial objects to form where such
differences already eliminated (strings converted to numbers, floats rounded
with same precision and so on).

But when initial objects must remain unchanged custom handlers may be used:
```
>>> from nested_diff import Differ, handlers
>>>
>>> class FloatHanler(handlers.TypeHandler):
...     handled_type = float
...
...     def __init__(self, precision=2, *args, **kwargs):
...         super().__init__(*args, **kwargs)
...         self.precision = precision
...
...     def diff(self, differ, a, b):
...         if round(a, self.precision) == round(b, self.precision):
...             return {'U': a} if differ.op_u else {}
...
...         return super().diff(differ, a, b)
>>>
>>>
>>> differ = Differ(U=False)
>>> differ.set_handler(FloatHanler(precision=1))
>>>
>>> a = [0.001, 0.01, 0.1]
>>> b = [0.002, 0.02, 0.2]
>>>
>>> assert {'D': [{'I': 2, 'N': 0.2, 'O': 0.1}]} == differ.diff(a, b)
>>>
```

Subclassing `Differ` is useful when objects with unequal types compared.
Example:
```
>>> from nested_diff import Differ
>>>
>>> class CustomDiffer(Differ):
...     def adjust_values(self, data):
...         return {k: int(v) for k, v in data.items()}
...
...     def diff(self, a, b):
...         return super().diff(
...             self.adjust_values(a),
...             self.adjust_values(b),
...         )
>>>
>>> a = {'one': 1, 'two': 2.0}
>>> b = {'one': '1', 'two': 2}
>>>
>>> assert CustomDiffer(U=False).diff(a, b) == {}  # no diff
>>>
```

## How to use nested\_diff tool with git

Ensure `nested_diff` command available, otherwise install it with `pip`
(relogin may be required afterwards):

`pip install --user nested_diff[cli]`

Add to `.gitconfig` following section:

```
[difftool "nested_diff"]
  cmd = nested_diff $LOCAL $REMOTE
```

and `ndiff = difftool --no-prompt --tool nested_diff` to section `[aliases]`.

Now `ndiff` subcommand available which may be used instead of `diff` when
nested diff required.
