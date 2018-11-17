"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/deeply_nested_sublist_removed_from_list.json
"""

from __future__ import unicode_literals
import nested_diff


def test_deeply_nested_sublist_removed_from_list():
    a = [0, [[0, 1]]]
    b = [0]
    diff = {'D': [{'U': 0}, {'R': [[0, 1]]}]}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
