"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/empty_hash_vs_empty_list.json
"""

from __future__ import unicode_literals
import nested_diff


def test_empty_hash_vs_empty_list():
    a = {}
    b = []
    diff = {'N': [], 'O': {}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
