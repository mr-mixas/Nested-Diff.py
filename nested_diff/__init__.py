# -*- coding: utf-8 -*-
#
# Copyright 2018-2021 Michael Samoglyadov
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
from difflib import SequenceMatcher
from pickle import dumps


__all__ = ['Differ', 'Iterator', 'Patcher', 'diff', 'patch']

__version__ = '0.7'
__author__ = 'Michael Samoglyadov'
__license__ = 'Apache License, Version 2.0'
__website__ = 'https://github.com/mr-mixas/Nested-Diff.py'


class Differ(object):
    """
    Compute recursive diff for two passed objects.

    Resulting diff is a dict and may contain following keys:
    `A` stands for 'added', it's value - added item.
    `D` means 'different' and contains subdiff.
    `E` diffed entity (optional), value - empty instance of entity's class.
    `I` index for sequence item, used only when prior item was omitted.
    `N` is a new value for changed item.
    `O` is a changed item's old value.
    `R` key used for removed item.
    `U` represent unchanged item.

    Diff metadata alternates with actual data; simple types specified as is,
    dicts, lists and tuples contain subdiffs for their items with native for
    such types addressing: indexes for lists and tuples and keys for
    dictionaries. Each status type, except `D`. `E` and `I`, may be omitted
    during diff computation. `E` tag is used with `D` when entity unable to
    contain diff by itself (set, frozenset); `D` contain a list of subdiffs
    in this case.

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
    def __init__(self, A=True, N=True, O=True, R=True, U=True,  # noqa: E741
                 trimR=False, diff_method=None, multiline_diff_context=-1):
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

        `multiline_diff_context` defines amount of context lines for multiline
        string diffs, multiline diffs disabled when value is negative.

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
            frozenset: self.diff_set,
            list: self.diff_list,
            set: self.diff_set,
            tuple: self.diff_tuple,
        }

        if multiline_diff_context >= 0:
            self.__differs[str] = self.diff_multiline
            self.multiline_diff_context = multiline_diff_context

    def diff(self, a, b):
        """
        Compute diff for two arbitrary objects.

        This method is a dispatcher and calls registered diff method for each
        diffed values pair according to their type. `diff__default` called for
        unequal and not registered types. Args and kwargs passed to called
        method as is.

        :param a: First object to diff.
        :param b: Second object to diff.

        """
        if self.__diff_method is not None:
            try:
                method = a.__getattribute__(self.__diff_method)
            except AttributeError:
                pass
            else:
                return method(
                    b,
                    A=self.op_a,
                    N=self.op_n,
                    O=self.op_o,  # noqa: E741
                    R=self.op_r,
                    U=self.op_u,
                    trimR=self.op_trim_r,
                    diff_method=self.__diff_method,
                )

        if a.__class__ is b.__class__:
            # it's faster to compare pickled dumps and dig differences
            # afterwards than recursively diff each pair of objects
            if a is b or dumps(a, -1) == dumps(b, -1):
                return {'U': a} if self.op_u else {}

            return self.get_differ(a.__class__)(a, b)

        return self.diff__default(a, b)

    def diff__default(self, a, b):
        """
        Return default diff.

        """
        dif = {}

        if self.op_n:
            dif['N'] = b
        if self.op_o:
            dif['O'] = a

        return dif

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

        for key in set(a).union(b):
            try:
                old = a[key]
                try:
                    new = b[key]
                except KeyError:  # removed
                    if self.op_r:
                        dif[key] = {'R': None if self.op_trim_r else old}
                    continue
            except KeyError:  # added
                if self.op_a:
                    dif[key] = {'A': b[key]}
                continue

            subdiff = self.diff(old, new)
            if subdiff:
                dif[key] = subdiff

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

    def diff_multiline(self, a, b):
        """
        Compute diff for multiline strings.

        Result is a unified diff formatted as usual nested diff structure with
        'I' tagged subdiffs to contain hunks headers.

        :param a: First string to diff.
        :param b: Second string to diff.

        >>> a = 'A\nB\nC'
        >>> b = 'A\nC'
        >>>
        >>> Differ(multiline_diff_context=3).diff_multiline(a, b)
        {'D': [{'I': [0, 3, 0, 2]}, {'U': 'A'}, {'R': 'B'}, {'U': 'C'}],
         'E': ''}

        """
        lines_a = a.split('\n', -1)
        lines_b = b.split('\n', -1)

        if len(lines_a) == len(lines_b) == 1:
            return self.diff__default(a, b)

        dif = []
        self.lcs.set_seq1(lines_a)
        self.lcs.set_seq2(lines_b)

        for group in self.lcs.get_grouped_opcodes(self.multiline_diff_context):
            dif.append({
                'I': [
                    group[0][1], group[-1][2],
                    group[0][3], group[-1][4],
                ],
            })

            for op, i1, i2, j1, j2 in group:
                if op == 'equal':
                    for line in lines_a[i1:i2]:
                        dif.append({'U': line})
                    continue

                if op in {'replace', 'delete'}:
                    for line in lines_a[i1:i2]:
                        dif.append({'R': line})

                if op in {'replace', 'insert'}:
                    for line in lines_b[j1:j2]:
                        dif.append({'A': line})

        if dif:
            return {'D': dif, 'E': a.__class__()}

        return {}

    def diff_set(self, a, b):
        """
        Compute diff for two [frozen]sets.

        :param a: First set to diff.
        :param b: Second set to diff.

        >>> a = {1, 2}
        >>> b = {2, 3}
        >>>
        >>> Differ(U=False).diff_sets(a, b)
        {'D': [{'R': 1}, {'A': 3}], 'E': set()}
        >>>

        """
        dif = []

        for i in a.union(b):
            if i in a and i in b:
                if self.op_u:
                    dif.append({'U': i})

            elif i in a:  # removed
                if self.op_r:
                    # ignore trimR opt here: value required for removal
                    dif.append({'R': i})

            else:  # added
                if self.op_a:
                    dif.append({'A': i})

        if dif:
            return {'D': dif, 'E': a.__class__()}

        return {}

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
        dif = self.diff_list(a, b)

        if 'D' in dif:
            dif['D'] = tuple(dif['D'])

        return dif

    def get_differ(self, type_):
        """
        Return diff method for specified type.

        :param type_: diffed object type.

        """
        try:
            return self.__differs[type_]
        except KeyError:
            return self.diff__default

    def set_differ(self, type_, method):
        """
        Set differ for specified data type.

        :param type_: diffed object type.
        :param method: diff method.

        """
        self.__differs[type_] = method


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
            str: self.patch_multiline,
            tuple: self.patch_tuple,
        }

    def get_patcher(self, type_):
        """
        Return patch method for specified type.

        :param type_: patched object type.

        """
        try:
            return self.__patchers[type_]
        except KeyError:
            raise NotImplementedError('unsupported diff type') from None

    def patch(self, target, ndiff):
        """
        Return patched object.

        This method is a dispatcher and calls apropriate patch method for
        target value according to it's type.

        :param target: Object to patch.
        :param ndiff: Nested diff.

        """
        if self.__patch_method is not None:
            try:
                method = target.__getattribute__(self.__patch_method)
            except AttributeError:
                pass
            else:
                return method(ndiff)

        if 'D' in ndiff:
            return self.get_patcher(
                ndiff['E' if 'E' in ndiff else 'D'].__class__,
            )(target, ndiff)
        elif 'N' in ndiff:
            return ndiff['N']

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

    def patch_multiline(self, target, ndiff):
        """
        Return patched multiline string.

        Unlike GNU patch, this algorithm does not implement any heuristics and
        patch target in straightforward way: get position from hunk header and
        apply changes specified in hunk.

        :param target: string to patch.
        :param ndiff: Nested diff.

        """
        offset = 0
        target = target.split('\n', -1)

        for subdiff in ndiff['D']:
            if 'I' in subdiff:  # hunk started
                idx = subdiff['I'][0] + offset
            elif 'A' in subdiff:
                target.insert(idx, subdiff['A'])
                offset = offset + 1
                idx = idx + 1
            elif 'R' in subdiff:
                if target.pop(idx) != subdiff['R']:
                    raise ValueError('Removing line does not match')
                offset = offset - 1
            elif 'U' in subdiff:
                if target[idx] != subdiff['U']:
                    raise ValueError('Unchanged line does not match')
                idx = idx + 1
            else:
                raise ValueError('Unsupported operation')

        return '\n'.join(target)

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

    def set_patcher(self, type_, method):
        """
        Set patcher for specified data type.

        :param type_: patched object type.
        :param method: patch method.

        """
        self.__patchers[type_] = method


class Iterator(object):
    """
    Nested diff iterator.

    """
    def __init__(self, sort_keys=False):
        """
        Construct iterator.

        If `sort_keys` is `True`, then the output for mappings will be
        sorted by key. Disabled by default.

        """
        self.sort_keys = sort_keys

        self.__iterators = {
            dict: self.iterate_mapping_diff,
            list: self.iterate_sequence_diff,
            tuple: self.iterate_sequence_diff,
        }

    @staticmethod
    def iterate__default(ndiff):
        """
        Yield final diff (do not iterate deeper).

        :param ndiff: nested diff.

        """
        yield ndiff, None, None

    def iterate_mapping_diff(self, ndiff):
        """
        Iterate over dict-like nested diffs.

        :param ndiff: nested diff.

        """
        items = ndiff['D'].items()

        for key, subdiff in sorted(items) if self.sort_keys else items:
            yield ndiff, key, subdiff

    @staticmethod
    def iterate_sequence_diff(ndiff):
        """
        Iterate over lists, tuples and alike nedsted diffs.

        :param ndiff: nested diff.

        """
        idx = 0

        for item in ndiff['D']:
            if 'I' in item:
                idx = item['I']

            yield ndiff, idx, item

            idx += 1

    def get_iterator(self, ndiff):
        """
        Return apropriate iterator for passed nested diff.

        :param ndiff: nested diff.

        """
        if 'E' in ndiff:
            return self.iterate__default(ndiff)

        try:
            return self.__iterators[ndiff['D'].__class__](ndiff)
        except KeyError:
            return self.iterate__default(ndiff)

    def set_iterator(self, type_, method):
        """
        Set generator for specified nested diff type.

        :param type_: type.
        :param method: method.

        Generator should yield tuples with three items: diff, key, and
        subdiff for this key.

        """
        self.__iterators[type_] = method

    def iterate(self, ndiff):
        """
        Yield tuples with diff, key and subdiff for each nested diff.

        :param ndiff: nested diff.

        """
        stack = [self.get_iterator(ndiff)]

        while stack:
            try:
                ndiff, key, subdiff = next(stack[-1])
            except StopIteration:
                stack.pop()
                continue

            yield ndiff, key, subdiff

            if subdiff is None:
                continue

            stack.append(self.get_iterator(subdiff))


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
