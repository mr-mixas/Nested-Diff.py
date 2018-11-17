"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/sublist_emptied.json
"""

from __future__ import unicode_literals
import nested_diff


def test_sublist_emptied():
    a = [[0]]
    b = [[]]
    diff = {'D': [{'D': [{'R': 0}]}]}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
