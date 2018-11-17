"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/sublist_filled_noA.json
"""

from __future__ import unicode_literals
import nested_diff


def test_sublist_filled_noA():
    a = [[]]
    b = [[0]]
    diff = {}
    opts = {'A': False}
    assert diff == nested_diff.diff(a, b, **opts)
