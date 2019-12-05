from nested_diff import diff
from nested_diff.fmt import TextFormatter


def test_equal():
    a = 'A\nB\nC'
    b = 'A\nB\nC'

    got = TextFormatter().format(diff(a, b, U=False, multiline_diff_context=3))

    assert '' == got


def test_line_added():
    a = 'B\nC'
    b = 'A\nB\nC'

    got = TextFormatter().format(diff(a, b, multiline_diff_context=3))
    expected = """\
# <str>
  @@ -1,2 +1,3 @@
+ A
  B
  C
"""
    assert expected == got


def test_line_changed():
    a = 'A\nB\nC'
    b = 'A\nb\nC'

    got = TextFormatter().format(diff(a, b, multiline_diff_context=3))
    expected = """\
# <str>
  @@ -1,3 +1,3 @@
  A
- B
+ b
  C
"""
    assert expected == got


def test_line_removed():
    a = 'A\nB\nC'
    b = 'A\nC'

    got = TextFormatter().format(diff(a, b, multiline_diff_context=3))
    expected = """\
# <str>
  @@ -1,3 +1,2 @@
  A
- B
  C
"""
    assert expected == got


def test_trailing_newlines():
    a = 'A\nB\n'
    b = 'A\nb\n'

    got = TextFormatter().format(diff(a, b, multiline_diff_context=3))
    expected = """\
# <str>
  @@ -1,3 +1,3 @@
  A
- B
+ b
  \n\
"""
    assert expected == got


def test_line_changed_ctx_0():
    a = 'A\nB\nC'
    b = 'A\nb\nC'

    got = TextFormatter().format(diff(a, b, multiline_diff_context=0))
    expected = """\
# <str>
  @@ -2 +2 @@
- B
+ b
"""
    assert expected == got
