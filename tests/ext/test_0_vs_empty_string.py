"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/0_vs_empty_string.json
"""

from __future__ import unicode_literals
import nested_diff


def test_0_vs_empty_string():
    a = 0
    b = ''
    diff = {'N': '', 'O': 0}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
