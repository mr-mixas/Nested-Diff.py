"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/empty_hash_vs_hash_with_one_key.json
"""

from __future__ import unicode_literals
import nested_diff


def test_empty_hash_vs_hash_with_one_key():
    a = {}
    b = {'one': 1}
    diff = {'D': {'one': {'A': 1}}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
