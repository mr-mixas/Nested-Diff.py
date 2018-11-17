"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_hashes_with_one_different_value.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_hashes_with_one_different_value():
    a = {'one': {'two': {'three': 3}}}
    b = {'one': {'two': {'three': 4}}}
    diff = {'D': {'one': {'D': {'two': {'D': {'three': {'N': 4, 'O': 3}}}}}}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
