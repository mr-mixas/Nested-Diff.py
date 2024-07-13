# Nested-Diff.py HowTo

## How to get shortest possible patch

```py
>>> from nested_diff import diff
>>>
>>> a = {'one': 1, 'two': 2, 'three': 'threeeeeeeee'}
>>> b = {'one': 1, 'two': 42}
>>>
>>> diff(a, b, O=False, U=False, trimR=True)
{'D': {'three': {'R': None}, 'two': {'N': 42}}}
>>>
```

## How to get unchanged items only

Diff calculates following changes by default:

* A: added items.
* N: new values for changed items.
* O: old values for changed items.
* R: removed items.
* U: unchanged items.

Thus disabling all except `U` diff will contain unchanged items only:

```py
>>> from nested_diff import Differ
>>>
>>> a = ['one', 'two', 'three']
>>> b = ['ONE', 'two']
>>>
>>> differ = Differ(A=False, N=False, O=False, R=False, U=True)
>>>
>>> is_equal, diff = differ.diff(a, b)
>>> is_equal
False
>>> diff
{'D': [{'U': 'two', 'I': 1}]}
>>>
```

## How to enable unified diffs for text values

```py
>>> from nested_diff import diff, handlers
>>> from nested_diff.formatters import TextFormatter
>>>
>>> a = 'one\ntwo\nthree'
>>> b = 'one\nthree'
>>>
>>> d =  diff(a, b, U=False, extra_handlers=[handlers.TextHandler(context=3)])
>>> d
{'D': [{'I': [0, 3, 0, 2]}, {'U': 'one'}, {'R': 'two'}, {'U': 'three'}], 'E': 5}
>>>
>>> print(TextFormatter().format(d))
# <str>
  @@ -1,3 +1,2 @@
  one
- two
  three
<BLANKLINE>
>>>
```

## How to render diff to HTML

```py
>>> from nested_diff import diff
>>> from nested_diff.formatters import HtmlFormatter
>>>
>>> a = ['a', 'b', 'c']
>>> b = ['A', 'b']
>>>
>>> formatter = HtmlFormatter()
>>> diff_ = diff(a, b)
>>>
>>> html_header = formatter.get_page_header(lang='en', title='Nested diff')
>>> html_body = formatter.format(diff_)
>>> html_footer = formatter.get_page_footer()
>>>
```

## How to diff objects with types unsupported by nested\_diff

External handlers may be set to support any desired types.  
Have a look at `Differ.set_handler` method for details and builtin set of
[nested\_diff.handlers](https://github.com/mr-mixas/Nested-Diff.py/tree/master/nested_diff/handlers.py)
for examples.

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

## How to treat NaNs as equals

```py
>>> from nested_diff import Differ, handlers
>>>
>>> differ = Differ()
>>> differ.set_handler(handlers.FloatHandler(nans_equal=True))
>>>
>>> differ.diff(float('nan'), float('nan'))
(True, {'U': nan})
>>>
```

## How to use nested\_diff tool with git

Ensure `nested_diff` command available, otherwise install it with `pip`:

`pip install --user nested_diff[cli]`

Add to `.gitconfig` following section:

```ini
[difftool "nested_diff"]
  cmd = HEADER_NAME_A="a/$MERGED" HEADER_NAME_B="b/$MERGED" \
        nested_diff $LOCAL $REMOTE
```

and `ndiff = difftool --no-prompt --tool nested_diff` to section `[aliases]`.

Now `ndiff` subcommand available and may be used in the same manner as `diff`.

## How to run tests locally

```sh
# prepare environment
python3 -m venv venv && \
    . venv/bin/activate && \
    pip install -e '.[cli,test]'

# run tests
pytest
```
