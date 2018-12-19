"""
Do not edit manually! Generated by tests/gen_ext_tests.py from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/hash_with_one_key_vs_empty_hash.json
"""

from __future__ import unicode_literals

import nested_diff


def test_diff():
    a = {'one': 1}
    b = {}
    diff = {'D': {'one': {'R': 1}}}
    opts = {}
    assert diff == nested_diff.diff(a, b, **opts)


def test_patch():
    a = {'one': 1}
    b = {}
    diff = {'D': {'one': {'R': 1}}}
    assert b == nested_diff.patch(a, diff)