"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/undef_vs_negative_number.json
"""

from __future__ import unicode_literals
import nested_diff


def test_undef_vs_negative_number():
    a = None
    b = -1
    diff = {'N': -1, 'O': None}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
