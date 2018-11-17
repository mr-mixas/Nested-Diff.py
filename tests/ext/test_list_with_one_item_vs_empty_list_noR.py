"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/list_with_one_item_vs_empty_list_noR.json
"""

from __future__ import unicode_literals
import nested_diff


def test_list_with_one_item_vs_empty_list_noR():
    a = [0]
    b = []
    diff = {}
    opts = {'R': False}
    assert diff == nested_diff.diff(a, b, **opts)
