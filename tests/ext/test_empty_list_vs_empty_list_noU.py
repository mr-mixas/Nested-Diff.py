"""
Do not edit manually! Generated from
https://github.com/mr-mixas/Nested-Diff/tree/master/tests/json/empty_list_vs_empty_list_noU.json
"""

from __future__ import unicode_literals
import nested_diff


def test_empty_list_vs_empty_list_noU():
    a = []
    b = []
    diff = {}
    opts = {'U': False}
    assert diff == nested_diff.diff(a, b, **opts)
