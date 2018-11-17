"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/hash_with_one_key_vs_empty_hash.json
"""

from __future__ import unicode_literals
import nested_diff


def test_hash_with_one_key_vs_empty_hash():
    a = {'one': 1}
    b = {}
    diff = {'D': {'one': {'R': 1}}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
