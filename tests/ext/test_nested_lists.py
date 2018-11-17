"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_lists.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_lists():
    a = [0, [[100]], [20, '30'], 4]
    b = [0, [[100]], [20, '31'], 5]
    diff = {'D': [{'U': 0}, {'U': [[100]]}, {'D': [{'U': 20}, {'N': '31', 'O': '30'}]}, {'N': 5, 'O': 4}]}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
