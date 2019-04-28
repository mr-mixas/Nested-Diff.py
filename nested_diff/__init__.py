# -*- coding: utf-8 -*-
#
# Copyright 2018,2019 Michael Samoglyadov
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


__all__ = ['Differ', 'Patcher', 'Walker', 'diff', 'patch']

__version__ = '0.4'
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
    def __init__(self, A=True, N=True, O=True, R=True, U=True, trimR=False,
                 diff_method=None):
        """
        Construct Differ.

        Optional arguments:
        `A`, `N`, `O`, `R`, `U` are toggles for according diff ops and all
        enabled (`True`) by default.

        `trimR` when True will drop (replace by `None`) removed data from diff;
        default is `False`.

        `diff_method` method with such name (if object have one) from first
        diffed object will be called for diff. Second diffed object and all
        Differ opts will be passed as arguments, diff expected for output.
        Disabled (`None`) by default.

        """
        self.__diff_method = diff_method
        self.lcs = SequenceMatcher(isjunk=None, autojunk=False)

        self.op_a = A
        self.op_n = N
        self.op_o = O
        self.op_r = R
        self.op_u = U
        self.op_trim_r = trimR

        self.__differs = {
            dict: self.diff_dict,
            frozenset: self.diff_frozenset,
            list: self.diff_list,
            set: self.diff_set,
            tuple: self.diff_tuple,
        }

    def diff(self, a, b):
        """
        Compute diff for two arbitrary objects.

        This method is a dispatcher and calls registered diff method for each
        diffed values pair according to their type. `diff__default` called for
        non-registered types. Args and kwargs passed to called method as is.

        :param a: First object to diff.
        :param b: Second object to diff.

        """
        if self.__diff_method is not None and hasattr(a, self.__diff_method):
            return getattr(a, self.__diff_method)(
                b,
                A=self.op_a,
                N=self.op_n,
                O=self.op_o,
                R=self.op_r,
                U=self.op_u,
                trimR=self.op_trim_r,
                diff_method=self.__diff_method,
            )

        if a.__class__ is b.__class__:
            if a == b:
                return {'U': a} if self.op_u else {}
            else:
                return self.get_differ(a.__class__)(a, b)

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

    def diff_dict(self, a, b):
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
        dif = {}

        for key in set(list(a) + list(b)):
            if key in a and key in b:
                if a[key] == b[key]:
                    if self.op_u:
                        dif[key] = {'U': a[key]}
                else:
                    subdiff = self.diff(a[key], b[key])
                    if subdiff:
                        dif[key] = subdiff

            elif key in a:  # removed
                if self.op_r:
                    dif[key] = {'R': None if self.op_trim_r else a[key]}

            else:  # added
                if self.op_a:
                    dif[key] = {'A': b[key]}

        if dif:
            return {'D': dif}

        return dif

    def diff_list(self, a, b):
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
        self.lcs.set_seq1(tuple(dumps(i, -1) for i in a))
        self.lcs.set_seq2(tuple(dumps(i, -1) for i in b))

        dif = []
        i = j = 0
        force_index = False

        for ai, bj, _ in self.lcs.get_matching_blocks():
            while i < ai and j < bj:
                subdiff = self.diff(a[i], b[j])
                if subdiff:
                    dif.append(subdiff)
                    if force_index:
                        dif[-1]['I'] = i
                        force_index = False
                else:
                    force_index = True

                i += 1
                j += 1

            while i < ai:  # removed
                if self.op_r:
                    dif.append({'R': None if self.op_trim_r else a[i]})
                    if force_index:
                        dif[-1]['I'] = i
                        force_index = False
                else:
                    force_index = True

                i += 1

            while j < bj:  # added
                if self.op_a:
                    dif.append({'A': b[j]})
                    if force_index:
                        dif[-1]['I'] = i
                        force_index = False
                else:
                    force_index = True

                j += 1

        if dif:
            return {'D': dif}

        return {}

    def diff_set(self, a, b):
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
        dif = set()

        for i in a.union(b):
            if i in a and i in b:
                if self.op_u:
                    dif.add(_hdict('U', i))

            elif i in a:  # removed
                if self.op_r:
                    dif.add(_hdict('R', None if self.op_trim_r else i))

            else:  # added
                if self.op_a:
                    dif.add(_hdict('A', i))

        if dif:
            return {'D': dif}

        return {}

    def diff_frozenset(self, a, b):
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
        ret = self.diff_set(a, b)

        if 'D' in ret:
            ret['D'] = frozenset(ret['D'])

        return ret

    def diff_tuple(self, a, b):
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
        ret = self.diff_list(a, b)

        if 'D' in ret:
            ret['D'] = tuple(ret['D'])

        return ret

    def get_differ(self, cls):
        """
        Return diff method for specified type.

        :param cls: diffed object type.

        """
        try:
            return self.__differs[cls]
        except KeyError:
            return self.diff__default

    def set_differ(self, cls, method):
        """
        Set differ for specified data type.

        :param cls: diffed object type.
        :param method: diff method.

        """
        self.__differs[cls] = method


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
    def __init__(self, patch_method=None):
        """
        Construct Patcher.

        Optional arguments:
        `patch_method` method with such name, if patched object have one, will
        be called with patch as argument. Patched object expected for output.
        Disabled (`None`) by default.

        """
        self.__patch_method = patch_method

        self.__patchers = {
            dict: self.patch_dict,
            frozenset: self.patch_frozenset,
            list: self.patch_list,
            set: self.patch_set,
            tuple: self.patch_tuple,
        }

    def get_patcher(self, cls):
        """
        Return patch method for specified type.

        :param cls: patched object type.

        """
        try:
            return self.__patchers[cls]
        except KeyError:
            raise NotImplementedError("unsupported object type")

    def patch(self, target, ndiff):
        """
        Return patched object.

        This method is a dispatcher and calls registered patch method for each
        patched value according to it's type. `patch__default` called for
        non-registered types. Args and kwargs passed to called method as is.

        :param target: Object to patch.
        :param ndiff: Nested diff.

        """
        if self.__patch_method is not None and \
           hasattr(target, self.__patch_method):
            return getattr(target, self.__patch_method)(ndiff)

        if 'D' in ndiff:
            return self.get_patcher(ndiff['D'].__class__)(target, ndiff)
        elif 'N' in ndiff:
            return ndiff['N']
        else:
            return target

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

    @staticmethod
    def patch_set(target, ndiff):
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

    def set_patcher(self, cls, method):
        """
        Set patcher for specified data type.

        :param cls: patched object type.
        :param method: patch method.

        """
        self.__patchers[cls] = method


class Walker(object):
    """
    Nested diff iterator.

    """
    def __init__(self, sort_keys=False):
        """
        Construct Walker.

        If `sort_keys` is `True`, then the output of dictionaries will be
        sorted by key. Disabled (Flase) by default.

        """
        self.sort_keys = sort_keys

        self.__iter_makers = {
            dict: self.make_iter_mapping,
            frozenset: self.make_iter_set,
            list: self.make_iter_sequence,
            set: self.make_iter_set,
            tuple: self.make_iter_sequence,
        }

    def get_iterator(self, value):
        try:
            make_iter = self.__iter_makers[value.__class__]
        except KeyError:
            raise NotImplementedError

        return make_iter(value)

    def make_iter_mapping(self, value):
        items = sorted(value.items()) if self.sort_keys else value.items()
        for key, val in items:
            yield key, val

    @staticmethod
    def make_iter_sequence(value):
        idx = 0
        for item in value:
            yield idx, item
            idx += 1

    @staticmethod
    def make_iter_set(value):
        for item in value:
            yield None, item

    def set_iter_maker(self, type_, method):
        """
        Set generator for specified data type.

        :param type_: data type.
        :param method: method.

        """
        self.__iter_makers[type_] = method

    def walk(self, ndiff):
        """
        Return tuple with depth, pointer and diff body for each nested subdiff.

        :param ndiff: Nested diff.

        """
        depth = 0
        stack = [((None, _) for _ in (ndiff,))]

        while stack:
            try:
                pointer, ndiff = next(stack[-1])
            except StopIteration:
                stack.pop()
                depth -= 1
                continue

            yield depth, pointer, ndiff

            if 'D' in ndiff:
                stack.append(self.get_iterator(ndiff['D']))
                depth += 1


def diff(a, b, **kwargs):
    """
    Compute recursive diff for two passed objects.

    Wrapper around Differ.diff() for backward compatibility.

    :param a: First object to diff.
    :param b: Second object to diff.

    See `__init__` in Differ class for kwargs specification.

    """
    return Differ(**kwargs).diff(a, b)


def patch(target, ndiff, **kwargs):
    """
    Return patched object.

    Wrapper around Patcher.patch() for backward compatibility.

    :param target: Object to patch.
    :param ndiff: Nested diff.

    See `__init__` in Patcher class for kwargs specification.

    """
    return Patcher(**kwargs).patch(target, ndiff)
