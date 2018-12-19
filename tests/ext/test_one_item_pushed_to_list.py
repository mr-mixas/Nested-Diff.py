"""
Do not edit manually! Generated by tests/gen_ext_tests.py from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/one_item_pushed_to_list.json
"""

from __future__ import unicode_literals

import nested_diff


def test_diff():
    a = [0]
    b = [0, 1]
    diff = {'D': [{'U': 0}, {'A': 1}]}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)


def test_patch():
    a = [0]
    b = [0, 1]
    diff = {'D': [{'U': 0}, {'A': 1}]}
    assert b == nested_diff.patch(a, diff)