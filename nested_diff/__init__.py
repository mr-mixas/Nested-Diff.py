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

from difflib import SequenceMatcher
from pickle import dumps


__all__ = ['Differ', 'Patcher', 'diff', 'patch']

__version__ = '0.3'
__author__ = 'Michael Samoglyadov'
__license__ = 'Apache License, Version 2.0'
__website__ = 'https://github.com/mr-mixas/Nested-Diff.py'


class Differ(object):
    """
    Compute recursive diff for two passed objects.

    Resulting diff is a dict and may contain following keys:
    `A` stands for 'added', it's value - added item.
    `D` means 'different' and contains subdiff.
    `I` index for sequence item, used only when prior item was omitted.
    `N` is a new value for changed item.
    `O` is a changed item's old value.
    `R` key used for removed item.
    `U` represent unchanged item.

    Diff metadata alternates with actual data; simple types specified as is,
    dicts, lists, sets and tuples contain subdiffs for their items with native
    for such types addressing: indexes for lists and tuples and keys for
    dictionaries. Each status type, except `D` and `I`, may be omitted during
    diff computation.

    Example:

    a:  {"one": [5,7]}
    b:  {"one": [5], "two": 2}
    opts: U=False  # omit unchanged items

    diff:
    {"D": {"one": {"D": [{"I": 1, "R": 7}]}, "two": {"A": 2}}}
    | |   |  |    | |   || |   |   |   |       |    | |   |
    | |   |  |    | |   || |   |   |   |       |    | |   +- with value 2
    | |   |  |    | |   || |   |   |   |       |    | +- key 'two' was added
    | |   |  |    | |   || |   |   |   |       |    +- subdiff for it
    | |   |  |    | |   || |   |   |   |       +- another key from top-level
    | |   |  |    | |   || |   |   |   +- what it was (item's value: 7)
    | |   |  |    | |   || |   |   +- what happened to item (removed)
    | |   |  |    | |   || |   +- list item's actual index
    | |   |  |    | |   || +- prior item was omitted
    | |   |  |    | |   |+- subdiff for list item
    | |   |  |    | |   +- it's value - list
    | |   |  |    | +- it is deeply changed
    | |   |  |    +- subdiff for key 'one'
    | |   |  +- it has key 'one'
    | |   +- top-level thing is a dict
    | +- changes somewhere deeply inside
    +- diff is always a dict

    Dicts, lists, sets and tuples traversed recursively, all other types
    compared by values.

    """
    def __init__(self, A=True, N=True, O=True, R=True, U=True, trimR=False):
        """
        Construct Differ.

        Optional arguments:
        `A`, `N`, `O`, `R`, `U` are toggles for according diff ops and all
        enabled (`True`) by default.

        `trimR` when True will drop (replace by `None`) removed data from diff;
        default is `False`.

        """
        self.lcs = SequenceMatcher(isjunk=None, autojunk=False)

        self.op_a = A
        self.op_n = N
        self.op_o = O
        self.op_r = R
        self.op_u = U
        self.op_trim_r = trimR

    def diff(self, a, b):
        """
        Compute diff for two arbitrary objects.

        This method is a dispatcher and calls `diff_dicts` for dicts,
        `diff_lists` for lists and so forth.

        :param a: First object to diff.
        :param b: Second object to diff.

        """
        if a == b:
            return {'U': a} if self.op_u else {}

        if isinstance(a, dict) and isinstance(a, type(b)):
            return self.diff_dicts(a, b)

        if isinstance(a, list) and isinstance(a, type(b)):
            return self.diff_lists(a, b)

        if isinstance(a, set) and isinstance(a, type(b)):
            return self.diff_sets(a, b)

        if isinstance(a, tuple) and isinstance(a, type(b)):
            return self.diff_tuples(a, b)

        if isinstance(a, frozenset) and isinstance(a, type(b)):
            return self.diff_frozensets(a, b)

        return self.diff__default(a, b)

    def diff__default(self, a, b):
        """
        Return default diff.

        """
        ret = {}

        if self.op_n:
            ret['N'] = b
        if self.op_o:
            ret['O'] = a

        return ret

    def diff_dicts(self, a, b):
        """
        Compute diff for two dicts.

        :param a: First dict to diff.
        :param b: Second dict to diff.

        >>> a = {'one': 1, 'two': 2, 'three': 3}
        >>> b = {'one': 1, 'two': 42}
        >>>
        >>> Differ(O=False, U=False).diff_dicts(a, b)
        {'D': {'two': {'N': 42}, 'three': {'R': 3}}}
        >>>

        """
        ret = {'D': {}}

        for key in set(list(a) + list(b)):
            if key in a and key in b:
                if a[key] == b[key]:
                    if self.op_u:
                        ret['D'][key] = {'U': a[key]}
                else:
                    subdiff = self.diff(a[key], b[key])
                    if subdiff:
                        ret['D'][key] = subdiff

            elif key in a:  # removed
                if self.op_r:
                    ret['D'][key] = {'R': None if self.op_trim_r else a[key]}

            else:  # added
                if self.op_a:
                    ret['D'][key] = {'A': b[key]}

        if not ret['D']:
            del ret['D']

        return ret

    def diff_lists(self, a, b):
        """
        Compute diff for two lists.

        :param a: First list to diff.
        :param b: Second list to diff.

        >>> a = [0,1,2,3]
        >>> b = [  1,2,4,5]
        >>>
        >>> Differ(O=False, U=False).diff_lists(a, b)
        {'D': [{'R': 0}, {'N': 4, 'I': 3}, {'A': 5}]}
        >>>

        """
        self.lcs.set_seq1([dumps(i, -1) for i in a])
        self.lcs.set_seq2([dumps(i, -1) for i in b])

        ret = {'D': []}
        i = j = 0
        force_index = False

        for ai, bj, _ in self.lcs.get_matching_blocks():
            while i < ai and j < bj:
                subdiff = self.diff(a[i], b[j])
                if subdiff:
                    ret['D'].append(subdiff)
                    if force_index:
                        ret['D'][-1]['I'] = i
                        force_index = False
                else:
                    force_index = True

                i += 1
                j += 1

            while i < ai:  # removed
                if self.op_r:
                    ret['D'].append({'R': None if self.op_trim_r else a[i]})
                    if force_index:
                        ret['D'][-1]['I'] = i
                        force_index = False
                else:
                    force_index = True

                i += 1

            while j < bj:  # added
                if self.op_a:
                    ret['D'].append({'A': b[j]})
                    if force_index:
                        ret['D'][-1]['I'] = i
                        force_index = False
                else:
                    force_index = True

                j += 1

        if not ret['D']:
            del ret['D']

        return ret

    def diff_sets(self, a, b):
        """
        Compute diff for two sets.

        :param a: First set to diff.
        :param b: Second set to diff.

        >>> a = {1, 2}
        >>> b = {2, 3}
        >>>
        >>> Differ(U=False).diff_sets(a, b)
        {'D': {{'R': 1}, {'A': 3}}}
        >>>

        """
        ret = {'D': set()}

        for i in a.union(b):
            if i in a and i in b:
                if self.op_u:
                    ret['D'].add(_hdict('U', i))

            elif i in a:  # removed
                if self.op_r:
                    ret['D'].add(_hdict('R', None if self.op_trim_r else i))

            else:  # added
                if self.op_a:
                    ret['D'].add(_hdict('A', i))

        if not ret['D']:
            del ret['D']

        return ret

    def diff_frozensets(self, a, b):
        """
        Compute diff for two frozen sets.

        :param a: First frozenset to diff.
        :param b: Second frozenset to diff.

        >>> a = frozenset((1, 2))
        >>> b = frozenset((2, 3))
        >>>
        >>> Differ(U=False).diff_frozensets(a, b)
        {'D': frozenset({{'R': 1}, {'A': 3}})}
        >>>

        """
        ret = self.diff_sets(a, b)

        if 'D' in ret:
            ret['D'] = frozenset(ret['D'])

        return ret

    def diff_tuples(self, a, b):
        """
        Compute diff for two tuples.

        :param a: First tuple to diff.
        :param b: Second tuple to diff.

        >>> a = (  1,2,4,5)
        >>> b = (0,1,2,3)
        >>>
        >>> Differ(O=False, U=False).diff_tuples(a, b)
        {'D': ({'A': 0}, {'N': 3, 'I': 2}, {'R': 5})}
        >>>

        """
        ret = self.diff_lists(a, b)

        if 'D' in ret:
            ret['D'] = tuple(ret['D'])

        return ret


class _hdict(dict):
    """
    Hashable dict, for internal use only.
    """
    def __init__(self, op, val):
        dict.__init__(self)
        self[op] = val
        self.__hash = hash((op, val))

    def __hash__(self):
        return self.__hash


class Patcher(object):
    """
    Patch objects using nested diff.

    """
    def patch(self, target, ndiff):
        """
        Return patched object.

        This method is a dispatcher and calls `patch_dict` for dicts,
        `patch_list` for lists and so forth.

        :param target: Object to patch.
        :param ndiff: Nested diff.

        """
        if 'D' in ndiff:
            if isinstance(ndiff['D'], dict):
                return self.patch_dict(target, ndiff)

            if isinstance(ndiff['D'], list):
                return self.patch_list(target, ndiff)

            if isinstance(ndiff['D'], set):
                return self.patch_set(target, ndiff)

            if isinstance(ndiff['D'], tuple):
                return self.patch_tuple(target, ndiff)

            if isinstance(ndiff['D'], frozenset):
                return self.patch_frozenset(target, ndiff)

            return self.patch__default(target, ndiff)

        elif 'N' in ndiff:
            return ndiff['N']

        else:
            return target

    def patch__default(self, target, ndiff):
        """
        Patch containers without dedicated methods.

        """
        raise NotImplementedError("unsupported object type")

    def patch_dict(self, target, ndiff):
        """
        Return patched dict.

        :param target: dict to patch.
        :param ndiff: Nested diff.

        """
        for key, subdiff in ndiff['D'].items():
            if 'D' in subdiff or 'N' in subdiff:
                target[key] = self.patch(target[key], subdiff)
            elif 'A' in subdiff:
                target[key] = subdiff['A']
            elif 'R' in subdiff:
                del target[key]

        return target

    def patch_list(self, target, ndiff):
        """
        Return patched list.

        :param target: list to patch.
        :param ndiff: Nested diff.

        """
        i, j = 0, 0  # index, scatter

        for subdiff in ndiff['D']:
            if 'I' in subdiff:
                i = subdiff['I'] + j

            if 'D' in subdiff or 'N' in subdiff:
                target[i] = self.patch(target[i], subdiff)
            elif 'A' in subdiff:
                target.insert(i, subdiff['A'])
                j += 1
            elif 'R' in subdiff:
                del target[i]
                j -= 1
                continue

            i += 1

        return target

    def patch_set(self, target, ndiff):
        """
        Return patched set.

        :param target: set to patch.
        :param ndiff: Nested diff.

        """
        for subdiff in ndiff['D']:
            if 'A' in subdiff:
                target.add(subdiff['A'])
            elif 'R' in subdiff:
                target.remove(subdiff['R'])

        return target

    def patch_tuple(self, target, ndiff):
        """
        Return patched tuple.

        :param target: tuple to patch.
        :param ndiff: Nested diff.

        """
        return tuple(self.patch_list(list(target), ndiff))

    def patch_frozenset(self, target, ndiff):
        """
        Return patched frozenset.

        :param target: frozenset to patch.
        :param ndiff: Nested diff.

        """
        return frozenset(self.patch_set(set(target), ndiff))


def diff(a, b, **kwargs):
    """
    Compute recursive diff for two passed objects.

    Wrapper around Differ.diff() for backward compatibility.

    :param a: First object to diff.
    :param b: Second object to diff.

    See `__init__` in Differ class for kwargs specification.

    """
    return Differ(**kwargs).diff(a, b)


def patch(target, ndiff):
    """
    Return patched object.

    Wrapper around Patcher.patch() for backward compatibility.

    :param target: Object to patch.
    :param ndiff: Nested diff.

    """
    return Patcher().patch(target, ndiff)
