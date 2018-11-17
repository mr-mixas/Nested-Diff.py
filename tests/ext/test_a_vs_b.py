"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/a_vs_b.json
"""

from __future__ import unicode_literals
import nested_diff


def test_a_vs_b():
    a = 'a'
    b = 'b'
    diff = {'N': 'b', 'O': 'a'}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
