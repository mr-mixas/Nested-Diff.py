"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/lists_LCS_removed_items_noU.json
"""

from __future__ import unicode_literals
import nested_diff


def test_lists_LCS_removed_items_noU():
    a = [0, 1, 2, 3, 4, 5, 6, 7]
    b = [2, 3, 5]
    diff = {'D': [{'R': 0}, {'R': 1}, {'R': 4, 'I': 4}, {'R': 6, 'I': 6}, {'R': 7}]}
    opts = {'U': False}
    assert diff == nested_diff.diff(a, b, **opts)
