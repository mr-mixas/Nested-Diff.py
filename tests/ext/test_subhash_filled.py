"""
Do not edit manually! Generated by tests/gen_ext_tests.py from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/subhash_filled.json
"""

from __future__ import unicode_literals

import nested_diff


def test_diff():
    a = {'one': {}}
    b = {'one': {'two': 2}}
    diff = {'D': {'one': {'D': {'two': {'A': 2}}}}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)


def test_patch():
    a = {'one': {}}
    b = {'one': {'two': 2}}
    diff = {'D': {'one': {'D': {'two': {'A': 2}}}}}
    assert b == nested_diff.patch(a, diff)