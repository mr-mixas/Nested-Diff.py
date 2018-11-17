"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/lists_with_one_different_item_noO.json
"""

from __future__ import unicode_literals
import nested_diff


def test_lists_with_one_different_item_noO():
    a = [0]
    b = [1]
    diff = {'D': [{'N': 1}]}
    opts = {'O': False}
    assert diff == nested_diff.diff(a, b, **opts)
