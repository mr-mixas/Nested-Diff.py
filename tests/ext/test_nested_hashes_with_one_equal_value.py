"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_hashes_with_one_equal_value.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_hashes_with_one_equal_value():
    a = {'one': {'two': {'three': 3}}}
    b = {'one': {'two': {'three': 3}}}
    diff = {'U': {'one': {'two': {'three': 3}}}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
