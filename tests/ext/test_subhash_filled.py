"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/subhash_filled.json
"""

from __future__ import unicode_literals
import nested_diff


def test_subhash_filled():
    a = {'one': {}}
    b = {'one': {'two': 2}}
    diff = {'D': {'one': {'D': {'two': {'A': 2}}}}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
