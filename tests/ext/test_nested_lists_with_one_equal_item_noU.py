"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_lists_with_one_equal_item_noU.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_lists_with_one_equal_item_noU():
    a = [[0]]
    b = [[0]]
    diff = {}
    opts = {'U': False}
    assert diff == nested_diff.diff(a, b, **opts)
