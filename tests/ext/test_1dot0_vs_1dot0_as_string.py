"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/1.0_vs_1.0_as_string.json
"""

from __future__ import unicode_literals
import nested_diff


def test_1dot0_vs_1dot0_as_string():
    a = 1
    b = '1.0'
    diff = {'N': '1.0', 'O': 1}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
