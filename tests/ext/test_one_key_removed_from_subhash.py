"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/one_key_removed_from_subhash.json
"""

from __future__ import unicode_literals
import nested_diff


def test_one_key_removed_from_subhash():
    a = {'one': {'two': 2, 'three': 3}}
    b = {'one': {'two': 2}}
    diff = {'D': {'one': {'D': {'two': {'U': 2}, 'three': {'R': 3}}}}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
