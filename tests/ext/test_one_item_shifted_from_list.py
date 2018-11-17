"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/one_item_shifted_from_list.json
"""

from __future__ import unicode_literals
import nested_diff


def test_one_item_shifted_from_list():
    a = [0, 1]
    b = [1]
    diff = {'D': [{'R': 0}, {'U': 1}]}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
