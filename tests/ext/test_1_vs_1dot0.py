"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/1_vs_1.0.json
"""

from __future__ import unicode_literals
import nested_diff


def test_1_vs_1dot0():
    a = 1
    b = 1
    diff = {'U': 1}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
