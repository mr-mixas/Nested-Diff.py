"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_lists_with_one_equal_item.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_lists_with_one_equal_item():
    a = [[0]]
    b = [[0]]
    diff = {'U': [[0]]}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
