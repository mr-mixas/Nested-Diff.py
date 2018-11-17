"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/lists_with_one_different_item_noN.json
"""

from __future__ import unicode_literals
import nested_diff


def test_lists_with_one_different_item_noN():
    a = [0]
    b = [1]
    diff = {'D': [{'O': 0}]}
    opts = {'N': False}
    assert diff == nested_diff.diff(a, b, **opts)
