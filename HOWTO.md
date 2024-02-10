# Nested-Diff.py HowTo

## How to diff objects with types unsupported by nested\_diff

Custom type handlers may be set to support any desired types, have a look at
`Differ.set_handler` method and [handlers.py](nested_diff/handlers.py).

## How to ignore some differences during diff

Most obvious and simple way is to transform initial objects to form where such
differences already eliminated (strings converted to numbers, floats rounded
with same precision and so on).

But when initial objects must remain unchanged custom handlers may be used:

```py
>>> from nested_diff import Differ, handlers
>>>
>>> class FloatHandler(handlers.FloatHandler):
...     def __init__(self, precision=2, *args, **kwargs):
...         super().__init__(*args, **kwargs)
...         self.precision = precision
...
...     def diff(self, differ, a, b):
...         if round(a, self.precision) == round(b, self.precision):
...             return True, {'U': a} if differ.op_u else {}
...
...         return super().diff(differ, a, b)
>>>
>>>
>>> differ = Differ(U=False)
>>> differ.set_handler(FloatHandler(precision=1))
>>>
>>> a = [0.001, 0.01, 0.1]
>>> b = [0.002, 0.02, 0.2]
>>>
assert differ.diff(a, b) == (False, {'D': [{'I': 2, 'N': 0.2, 'O': 0.1}]})
>>>
```

## How to use nested\_diff tool with git

Ensure `nested_diff` command available, otherwise install it with `pip`:

`pip install --user nested_diff[cli]`

Add to `.gitconfig` following section:

```ini
[difftool "nested_diff"]
  cmd = nested_diff $LOCAL $REMOTE
```

and `ndiff = difftool --no-prompt --tool nested_diff` to section `[aliases]`.

Now `ndiff` subcommand available and may be used in the same manner as `diff`.

### How to run tests locally

```sh
# prepare environment
python3 -m venv venv && \
    . venv/bin/activate && \
    pip install -e '.[cli,test]'

# run tests
pytest
```
