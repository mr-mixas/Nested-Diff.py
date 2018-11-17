"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/one_key_added_to_subhash_noU.json
"""

from __future__ import unicode_literals
import nested_diff


def test_one_key_added_to_subhash_noU():
    a = {'one': {'two': 2}}
    b = {'one': {'two': 2, 'three': 3}}
    diff = {'D': {'one': {'D': {'three': {'A': 3}}}}}
    opts = {'U': False}
    assert diff == nested_diff.diff(a, b, **opts)
