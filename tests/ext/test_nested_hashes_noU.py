"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/nested_hashes_noU.json
"""

from __future__ import unicode_literals
import nested_diff


def test_nested_hashes_noU():
    a = {'two': {'nine': 9, 'ten': 10}, 'one': 1, 'three': 3}
    b = {'one': 1, 'four': 4, 'two': {'nine': 8, 'ten': 10}}
    diff = {'D': {'two': {'D': {'nine': {'N': 8, 'O': 9}}}, 'four': {'A': 4}, 'three': {'R': 3}}}
    opts = {'U': False}
    assert diff == nested_diff.diff(a, b, **opts)
