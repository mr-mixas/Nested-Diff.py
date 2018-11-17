"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/empty_string_vs_undef.json
"""

from __future__ import unicode_literals
import nested_diff


def test_empty_string_vs_undef():
    a = ''
    b = None
    diff = {'N': None, 'O': ''}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
