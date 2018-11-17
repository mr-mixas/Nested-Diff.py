"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/one_key_added_to_subhash.json
"""

from __future__ import unicode_literals
import nested_diff


def test_one_key_added_to_subhash():
    a = {'one': {'two': 2}}
    b = {'one': {'two': 2, 'three': 3}}
    diff = {'D': {'one': {'D': {'two': {'U': 2}, 'three': {'A': 3}}}}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
