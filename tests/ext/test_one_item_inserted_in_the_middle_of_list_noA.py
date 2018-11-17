"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/one_item_inserted_in_the_middle_of_list_noA.json
"""

from __future__ import unicode_literals
import nested_diff


def test_one_item_inserted_in_the_middle_of_list_noA():
    a = [0, 2]
    b = [0, 1, 2]
    diff = {'D': [{'U': 0}, {'U': 2, 'I': 1}]}
    opts = {'A': False}
    assert diff == nested_diff.diff(a, b, **opts)
