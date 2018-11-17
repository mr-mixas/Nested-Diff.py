"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_mixed_structures.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_mixed_structures():
    a = {'one': [{'two': {'three': [7, 4]}}, 8]}
    b = {'one': [{'two': {'three': [7, 3]}}, 8]}
    diff = {'D': {'one': {'D': [{'D': {'two': {'D': {'three': {'D': [{'U': 7}, {'N': 3, 'O': 4}]}}}}}, {'U': 8}]}}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
