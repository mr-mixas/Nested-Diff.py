"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/subhash_filled_noA.json
"""

from __future__ import unicode_literals
import nested_diff


def test_subhash_filled_noA():
    a = {'one': {}}
    b = {'one': {'two': 2}}
    diff = {}
    opts = {'A': False}
    assert diff == nested_diff.diff(a, b, **opts)
