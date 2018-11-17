"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/empty_hash_vs_empty_hash.json
"""

from __future__ import unicode_literals
import nested_diff


def test_empty_hash_vs_empty_hash():
    a = {}
    b = {}
    diff = {'U': {}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
