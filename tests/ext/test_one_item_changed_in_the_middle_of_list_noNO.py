"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/one_item_changed_in_the_middle_of_list_noNO.json
"""

from __future__ import unicode_literals
import nested_diff


def test_one_item_changed_in_the_middle_of_list_noNO():
    a = [0, 1, 2]
    b = [0, 9, 2]
    diff = {'D': [{'U': 0}, {'U': 2, 'I': 2}]}
    opts = {'N': False, 'O': False}
    assert diff == nested_diff.diff(a, b, **opts)
