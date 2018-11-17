"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/empty_string_vs_0.json
"""

from __future__ import unicode_literals
import nested_diff


def test_empty_string_vs_0():
    a = ''
    b = 0
    diff = {'N': 0, 'O': ''}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
