"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_lists_LCS.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_lists_LCS():
    a = ['a', 'b', 'c', 'e', 'h', 'j', 'l', 'm', 'n', 'p']
    b = ['b', 'c', 'd', 'e', 'f', 'j', 'k', 'l', 'm', 'r', 's', 't']
    diff = {'D': [{'R': 'a'}, {'U': 'b'}, {'U': 'c'}, {'A': 'd'}, {'U': 'e'}, {'N': 'f', 'O': 'h'}, {'U': 'j'}, {'A': 'k'}, {'U': 'l'}, {'U': 'm'}, {'N': 'r', 'O': 'n'}, {'N': 's', 'O': 'p'}, {'A': 't'}]}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)
