"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/deeply_nested_list_vs_empty_list_trimR.json
"""

from __future__ import unicode_literals
import nested_diff


def test_deeply_nested_list_vs_empty_list_trimR():
    a = [[[0, 1]]]
    b = []
    diff = {'D': [{'R': None}]}
    opts = {'trimR': True}
    assert diff == nested_diff.diff(a, b, **opts)
