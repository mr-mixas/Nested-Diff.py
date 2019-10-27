import pytest

from nested_diff import diff
from nested_diff.fmt import TextFormatter


def test_numbers_diff():
    a = 0
    b = 1

    got = TextFormatter().format(diff(a, b))
    expected = """\
- 0
+ 1
"""
    assert expected == got


def test_strings_diff():
    a = 'A'
    b = 'B'

    got = TextFormatter().format(diff(a, b))
    expected = """\
- 'A'
+ 'B'
"""
    assert expected == got


def test_escaped_string_values():
    a = 'A\n'
    b = 'A\t'

    got = TextFormatter().format(diff(a, b))
    expected = """\
- 'A\\n'
+ 'A\\t'
"""
    assert expected == got


def test_lists_diff():
    a = [0, [1], 3]
    b = [0, [1, 2], 3]

    got = TextFormatter().format(diff(a, b))

    expected = """\
  [0]
    0
  [1]
    [0]
      1
+   [1]
+     2
  [2]
    3
"""

    assert expected == got


def test_lists_diff_noU():
    a = [0, [1], 3]
    b = [0, [1, 2], 3]

    got = TextFormatter().format(diff(a, b, U=False))

    expected = """\
  [1]
+   [1]
+     2
"""

    assert expected == got


def test_tuples_diff():
    a = (0, (1,), 3)
    b = (0, (1, 2), 3)

    got = TextFormatter().format(diff(a, b))

    expected = """\
  (0)
    0
  (1)
    (0)
      1
+   (1)
+     2
  (2)
    3
"""

    assert expected == got


def test_substructures_repr():
    a = [[[[0]], 8], [2]]
    b = [[[[0]], 8], [3]]

    got = TextFormatter().format(diff(a, b))

    expected = """\
  [0]
    [[[0]], 8]
  [1]
    [0]
-     2
+     3
"""

    assert expected == got


def test_dicts_diff():
    a = {'one': 1, 'three': 3, 'four': {'forty\ttwo': 42}, 'five': 5}
    b = {'two': 2, 'three': 3, 'four': {'forty\ntwo': 42}, 'five': 7}

    got = TextFormatter(sort_keys=True).format(diff(a, b))

    expected = """\
  {'five'}
-   5
+   7
  {'four'}
-   {'forty\\ttwo'}
-     42
+   {'forty\\ntwo'}
+     42
- {'one'}
-   1
  {'three'}
    3
+ {'two'}
+   2
"""

    assert expected == got


def test_dicts_diff_noU():
    a = {'one': 1, 'three': 3, 'four': {'forty\ttwo': 42}, 'five': 5}
    b = {'two': 2, 'three': 3, 'four': {'forty\ntwo': 42}, 'five': 7}

    got = TextFormatter(sort_keys=True).format(diff(a, b, U=False))

    expected = """\
  {'five'}
-   5
+   7
  {'four'}
-   {'forty\\ttwo'}
-     42
+   {'forty\\ntwo'}
+     42
- {'one'}
-   1
+ {'two'}
+   2
"""

    assert expected == got


def test_sets_diff():
    a = {'a'}
    b = {'a', 'b'}

    got = TextFormatter().format(diff(a, b))

    expected = {
        """\
  <set>
    'a'
+   'b'
""",
        """\
  <set>
+   'b'
    'a'
""",
    }

    assert got in expected


def test_frozensets_diff():
    a = frozenset(('a',))
    b = frozenset(('a', 'b'))

    got = TextFormatter().format(diff(a, b))
    expected = {
        """\
  <frozenset>
    'a'
+   'b'
""",
        """\
  <frozenset>
+   'b'
    'a'
""",
    }

    assert got in expected


def test_mixed_structures_diff():
    a = {'one': [{'two': 2}, 3, set()]}
    b = {'one': [{'two': 0}, 4, {True}]}

    got = TextFormatter().format(diff(a, b))
    expected = """\
  {'one'}
    [0]
      {'two'}
-       2
+       0
    [1]
-     3
+     4
    [2]
      <set>
+       True
"""

    assert expected == got


def test_emitter_absent():
    with pytest.raises(NotImplementedError):
        TextFormatter().format({'D': [], 'E': None})


def test_wrappings():
    a = 0
    b = 1

    got = TextFormatter().format(
        diff(a, b),
        header='Header',
        footer='Footer',
    )
    print(got)
    expected = """\
Header
- 0
+ 1
Footer
"""
    assert expected == got
