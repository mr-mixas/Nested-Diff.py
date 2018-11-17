"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/hash_with_one_key_vs_empty_hash_noR.json
"""

from __future__ import unicode_literals
import nested_diff


def test_hash_with_one_key_vs_empty_hash_noR():
    a = {'one': 1}
    b = {}
    diff = {}
    opts = {'R': False}
    assert diff == nested_diff.diff(a, b, **opts)
