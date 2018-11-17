"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/empty_hash_vs_hash_with_one_key_noA.json
"""

from __future__ import unicode_literals
import nested_diff


def test_empty_hash_vs_hash_with_one_key_noA():
    a = {}
    b = {'one': 1}
    diff = {}
    opts = {'A': False}
    assert diff == nested_diff.diff(a, b, **opts)
