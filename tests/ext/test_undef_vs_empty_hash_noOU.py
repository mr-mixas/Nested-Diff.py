"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/undef_vs_empty_hash_noOU.json
"""

from __future__ import unicode_literals
import nested_diff


def test_undef_vs_empty_hash_noOU():
    a = None
    b = {}
    diff = {}
    opts = {'N': False, 'O': False}
    assert diff == nested_diff.diff(a, b, **opts)
