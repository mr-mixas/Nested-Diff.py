"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/empty_list_vs_deeply_nested_list.json
"""

from __future__ import unicode_literals
import nested_diff


def test_empty_list_vs_deeply_nested_list():
    a = []
    b = [[[0, 1]]]
    diff = {'D': [{'A': [[0, 1]]}]}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
