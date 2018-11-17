"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/lists_LCS_added_items.json
"""

from __future__ import unicode_literals
import nested_diff


def test_lists_LCS_added_items():
    a = [2, 3, 5]
    b = [0, 1, 2, 3, 4, 5, 6, 7]
    diff = {'D': [{'A': 0}, {'A': 1}, {'U': 2}, {'U': 3}, {'A': 4}, {'U': 5}, {'A': 6}, {'A': 7}]}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
