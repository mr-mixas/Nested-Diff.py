"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/hashes_with_one_different_value_noN.json
"""

from __future__ import unicode_literals
import nested_diff


def test_hashes_with_one_different_value_noN():
    a = {'one': 1}
    b = {'one': 2}
    diff = {'D': {'one': {'O': 1}}}
    opts = {'N': False}
    assert diff == nested_diff.diff(a, b, **opts)
