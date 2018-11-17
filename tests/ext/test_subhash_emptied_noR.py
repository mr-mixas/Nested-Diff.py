"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/subhash_emptied_noR.json
"""

from __future__ import unicode_literals
import nested_diff


def test_subhash_emptied_noR():
    a = {'one': {'two': 2}}
    b = {'one': {}}
    diff = {}
    opts = {'R': False}
    assert diff == nested_diff.diff(a, b, **opts)
