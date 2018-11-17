"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_lists_LCS_onlyU.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_lists_LCS_onlyU():
    a = ['a', 'b', 'c', 'e', 'h', 'j', 'l', 'm', 'n', 'p']
    b = ['b', 'c', 'd', 'e', 'f', 'j', 'k', 'l', 'm', 'r', 's', 't']
    diff = {'D': [{'U': 'b', 'I': 1}, {'U': 'c'}, {'U': 'e', 'I': 3}, {'U': 'j', 'I': 5}, {'U': 'l', 'I': 6}, {'U': 'm'}]}
    opts = {'R': False, 'O': False, 'N': False, 'A': False}
    assert diff == nested_diff.diff(a, b, **opts)
