"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/a_vs_a.json
"""

from __future__ import unicode_literals
import nested_diff


def test_a_vs_a():
    a = 'a'
    b = 'a'
    diff = {'U': 'a'}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
