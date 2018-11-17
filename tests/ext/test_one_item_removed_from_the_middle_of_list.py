"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/one_item_removed_from_the_middle_of_list.json
"""

from __future__ import unicode_literals
import nested_diff


def test_one_item_removed_from_the_middle_of_list():
    a = [0, 1, 2]
    b = [0, 2]
    diff = {'D': [{'U': 0}, {'R': 1}, {'U': 2}]}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
