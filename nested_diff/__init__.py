# -*- coding: utf-8 -*-
#
# Copyright 2018 Michael Samoglyadov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Recursive diff for nested structures, implementation of
https://github.com/mr-mixas/Nested-Diff

"""

from __future__ import unicode_literals

from difflib import SequenceMatcher as LCS
from pickle import dumps


__all__ = ['diff', 'patch']

__version__ = '0.1'
__author__  = 'Michael Samoglyadov'
__website__ = ''
__license__ = 'Apache License, Version 2.0'


def diff(a, b, **kwargs):
    if a == b:
        ret = {'U': a}
    elif isinstance(a, dict) and isinstance(a, type(b)):
        ret = {'D': {}}

        for k in set(list(a) + list(b)):
            if k in a and k in b:
                if a[k] == b[k]:
                    ret['D'][k] = {'U': a[k]}
                else:  # dig subdiff
                    ret['D'][k] = diff(a[k], b[k], **kwargs)

            elif k in a:  # removed
                ret['D'][k] = {'R': a[k]}

            elif k in b:  # added
                ret['D'][k] = {'A': b[k]}

    elif isinstance(a, list) and isinstance(a, type(b)):
        lcs = LCS(None, [dumps(i) for i in a], [dumps(i) for i in b])

        ret = {'D': []}
        i = j = 0

        for ai, bj, _ in lcs.get_matching_blocks():
            while i < ai and j < bj:  # dig subdiff
                ret['D'].append(diff(a[i], b[j], **kwargs))
                i += 1
                j += 1

            while i < ai:  # removed
                ret['D'].append({'R': a[i]})
                i += 1

            while j < bj:  # added
                ret['D'].append({'A': b[j]})
                j += 1

    else:
        ret = {'N': b, 'O': a}

    return ret


def patch(target, patch):
    raise NotImplementedError()
