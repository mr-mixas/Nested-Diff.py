"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/one_item_unshifted_to_list_noU.json
"""

from __future__ import unicode_literals
import nested_diff


def test_one_item_unshifted_to_list_noU():
    a = [1]
    b = [0, 1]
    diff = {'D': [{'A': 0}]}
    opts = {'U': False}
    assert diff == nested_diff.diff(a, b, **opts)
