"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/undef_vs_undef.json
"""

from __future__ import unicode_literals
import nested_diff


def test_undef_vs_undef():
    a = None
    b = None
    diff = {'U': None}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
