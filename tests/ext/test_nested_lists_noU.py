"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_lists_noU.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_lists_noU():
    a = [0, [[100]], [20, '30'], 4]
    b = [0, [[100]], [20, '31'], 5]
    diff = {'D': [{'D': [{'N': '31', 'O': '30', 'I': 1}], 'I': 2}, {'N': 5, 'O': 4}]}
    opts = {'U': False}
    assert diff == nested_diff.diff(a, b, **opts)
