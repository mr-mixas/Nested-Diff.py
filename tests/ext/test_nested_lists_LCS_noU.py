"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_lists_LCS_noU.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_lists_LCS_noU():
    a = ['a', 'b', 'c', 'e', 'h', 'j', 'l', 'm', 'n', 'p']
    b = ['b', 'c', 'd', 'e', 'f', 'j', 'k', 'l', 'm', 'r', 's', 't']
    diff = {'D': [{'R': 'a'}, {'I': 3, 'A': 'd'}, {'N': 'f', 'O': 'h', 'I': 4}, {'I': 6, 'A': 'k'}, {'N': 'r', 'O': 'n', 'I': 8}, {'N': 's', 'O': 'p'}, {'A': 't'}]}
    opts = {'U': False}
    assert diff == nested_diff.diff(a, b, **opts)
