"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_hashes_with_one_equal_value_noU.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_hashes_with_one_equal_value_noU():
    a = {'one': {'two': {'three': 3}}}
    b = {'one': {'two': {'three': 3}}}
    diff = {}
    opts = {'U': False}
    assert diff == nested_diff.diff(a, b, **opts)
