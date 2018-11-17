"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/subhash_emptied.json
"""

from __future__ import unicode_literals
import nested_diff


def test_subhash_emptied():
    a = {'one': {'two': 2}}
    b = {'one': {}}
    diff = {'D': {'one': {'D': {'two': {'R': 2}}}}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
