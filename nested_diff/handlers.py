# -*- coding: utf-8 -*-
#
# Copyright 2022 Michael Samoglyadov
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

"""Type handlers for nedted diff."""

from difflib import SequenceMatcher
from pickle import dumps


class TypeHandler(object):
    """
    Base class for type handlers.

    Handlers provide diff, patch, generate_formatted_diff and iterate_diff
    methods for specific type.

    """

    handled_type = None

    type_prefix = ''
    type_suffix = ''

    def diff(self, differ, a, b):
        """
        Return equality flag and diff for two objects.

        :param differ: nested_diff.Differ object.
        :param a: First dict to diff.
        :param b: Second dict to diff.

        """
        diff = {}
        equal = True

        if dumps(a, -1) == dumps(b, -1):
            if differ.op_u:
                diff['U'] = a
        else:
            if differ.op_n:
                diff['N'] = b
            if differ.op_o:
                diff['O'] = a
            equal = False

        return equal, diff

    def patch(self, patcher, target, diff):
        """
        Return patched object.

        :param patcher: nested_diff.Patcher object.
        :param target: Object to patch.
        :param diff: Nested diff.

        """
        try:
            return diff['N']
        except KeyError:
            if not diff or 'U' in diff:
                return target

        raise ValueError(diff)

    def iterate_diff(self, iterator, diff):
        """
        Iterate over nested diff.

        :param patcher: nested_diff.Iterator object.
        :param diff: Nested diff.

        """
        yield diff, None, None

    def generate_formatted_diff(self, formatter, diff, depth):
        """Generate formatted diff."""
        for tag in formatter.tags:
            try:
                value = diff[tag]
            except KeyError:
                continue

            yield from formatter.generate_value(value, tag, depth)


class ScalarHandler(TypeHandler):
    """Base class for scalar handlers."""

    def diff(self, differ, a, b):
        """
        Return diff for two scalar objects.

        :param differ: nested_diff.Differ object.
        :param a: First dict to diff.
        :param b: Second dict to diff.

        """
        diff = {}
        equal = True

        if a == b:
            if differ.op_u:
                diff['U'] = a
        else:
            if differ.op_n:
                diff['N'] = b
            if differ.op_o:
                diff['O'] = a
            equal = False

        return equal, diff


class IntHandler(ScalarHandler):
    """int handler."""

    handled_type = int


class FloatHandler(ScalarHandler):
    """float handler."""

    handled_type = float


class StrHandler(ScalarHandler):
    """str handler."""

    handled_type = str


class BytesHandler(ScalarHandler):
    """bytes handler."""

    handled_type = bytes


class DictHandler(TypeHandler):
    """dict handler."""

    handled_type = dict

    type_prefix = '{'
    type_suffix = '}'

    def diff(self, differ, a, b):
        """
        Return equality flag and diff for two dicts.

        :param differ: nested_diff.Differ object.
        :param a: First dict to diff.
        :param b: Second dict to diff.

        >>> from nested_diff import Differ
        >>>
        >>> a = {'one': 1, 'two': 2, 'three': 3}
        >>> b = {'one': 1, 'two': 42}
        >>>
        >>> Differ(handlers=[DictHandler()], O=False, U=False).diff(a, b)
        (False, {'D': {'three': {'R': 3}, 'two': {'N': 42}}})
        >>>
        """
        diff = {}
        equal = True

        for key in set(a).union(b):
            try:
                old = a[key]
                try:
                    new = b[key]
                except KeyError:  # removed
                    if differ.op_r:
                        diff[key] = {'R': None if differ.op_trim_r else old}

                    equal = False
                    continue
            except KeyError:  # added
                if differ.op_a:
                    diff[key] = {'A': b[key]}

                equal = False
                continue

            subequal, subdiff = differ.diff(old, new)

            if not subequal:
                equal = False

            if subdiff:
                diff[key] = subdiff

        if diff:
            if equal:
                diff = {'U': a}
            else:
                diff = {'D': diff}
        elif equal and differ.op_u:
            diff = {'U': a}

        return equal, diff

    def patch(self, patcher, target, diff):
        """
        Return patched dict.

        :param patcher: nested_diff.Patcher object.
        :param target: dict to patch.
        :param diff: nested diff.

        """
        for key, subdiff in diff['D'].items():
            if 'D' in subdiff or 'N' in subdiff:
                target[key] = patcher.patch(target[key], subdiff)
            elif 'A' in subdiff:
                target[key] = subdiff['A']
            elif 'R' in subdiff:
                del target[key]

        return target

    def iterate_diff(self, iterator, diff):
        """
        Iterate over dict diff.

        :param iterator: nested_diff.Iterator object.
        :param diff: nested diff.

        """
        items = diff['D'].items()

        for key, subdiff in sorted(items) if iterator.sort_keys else items:
            yield diff, key, subdiff

    def generate_formatted_diff(self, formatter, diff, depth):
        """Generate formatted dict diff."""
        items = diff['D'].items()

        for key, subdiff in sorted(items) if formatter.sort_keys else items:
            for tag in formatter.tags:
                if tag in subdiff:
                    yield from formatter.generate_key(
                        key, tag, self.handled_type, depth,
                    )
                    break

            yield from formatter.generate_diff(subdiff, depth=depth+1)


class ListHandler(TypeHandler):
    """list handler."""

    handled_type = list

    type_prefix = '['
    type_suffix = ']'

    def __init__(self):
        """Initialize handler."""
        super().__init__()
        self.lcs = SequenceMatcher(isjunk=None, autojunk=False)

    def diff(self, differ, a, b):
        """
        Return equality flag and diff for two lists.

        :param differ: nested_diff.Differ object.
        :param a: First list to diff.
        :param b: Second list to diff.

        >>> from nested_diff import Differ
        >>>
        >>> a = [0,1,2,3]
        >>> b = [  1,2,4,5]
        >>>
        >>> Differ(handlers=[ListHandler()], O=False, U=False).diff(a, b)
        (False, {'D': [{'R': 0}, {'N': 4, 'I': 3}, {'A': 5}]})
        >>>
        """
        self.lcs.set_seq1(tuple(dumps(i, -1) for i in a))
        self.lcs.set_seq2(tuple(dumps(i, -1) for i in b))

        diff = []
        equal = True
        i = j = 0
        force_index = False

        for ai, bj, _ in self.lcs.get_matching_blocks():
            while i < ai and j < bj:
                subequal, subdiff = differ.diff(a[i], b[j])
                if subdiff:
                    diff.append(subdiff)
                    if force_index:
                        diff[-1]['I'] = i
                        force_index = False
                else:
                    force_index = True

                if not subequal:
                    equal = False

                i += 1
                j += 1

            while i < ai:  # removed
                if differ.op_r:
                    diff.append({'R': None if differ.op_trim_r else a[i]})
                    if force_index:
                        diff[-1]['I'] = i
                        force_index = False
                else:
                    force_index = True

                equal = False
                i += 1

            while j < bj:  # added
                if differ.op_a:
                    diff.append({'A': b[j]})
                    if force_index:
                        diff[-1]['I'] = i
                        force_index = False
                else:
                    force_index = True

                equal = False
                j += 1

        if diff:
            if equal:
                return equal, {'U': a}
            return equal, {'D': diff}
        elif equal and differ.op_u:
            return equal, {'U': a}

        return equal, {}

    def patch(self, patcher, target, diff):
        """
        Return patched list.

        :param patcher: nested_diff.Patcher object.
        :param target: list to patch.
        :param diff: Nested diff.

        """
        i, j = 0, 0  # index, scatter

        for subdiff in diff['D']:
            if 'I' in subdiff:
                i = subdiff['I'] + j

            if 'D' in subdiff or 'N' in subdiff:
                target[i] = patcher.patch(target[i], subdiff)
            elif 'A' in subdiff:
                target.insert(i, subdiff['A'])
                j += 1
            elif 'R' in subdiff:
                del target[i]
                j -= 1
                continue

            i += 1

        return target

    def iterate_diff(self, iterator, diff):
        """
        Iterate over list diff.

        :param diff: nested diff.

        """
        idx = 0

        for item in diff['D']:
            try:
                idx = item['I']
            except KeyError:
                pass

            yield diff, idx, item

            idx += 1

    def generate_formatted_diff(self, formatter, diff, depth):
        """Generate formatted list diff."""
        idx = 0

        for subdiff in diff['D']:
            try:
                idx = subdiff['I']
            except KeyError:
                pass

            for tag in formatter.tags:
                if tag in subdiff:
                    yield from formatter.generate_key(
                        idx, tag, self.handled_type, depth,
                    )
                    break

            yield from formatter.generate_diff(subdiff, depth=depth+1)

            idx += 1


class TupleHandler(ListHandler):
    """tuple handler."""

    handled_type = tuple

    type_prefix = '('
    type_suffix = ')'

    def diff(self, differ, a, b):
        """
        Return equality flag and diff for two tuples.

        :param differ: nested_diff.Differ object.
        :param a: First tuple to diff.
        :param b: Second tuple to diff.

        >>> from nested_diff import Differ
        >>>
        >>> a = (  1,2,4,5)
        >>> b = (0,1,2,3)
        >>>
        >>> Differ(handlers=[TupleHandler()], O=False, U=False).diff(a, b)
        (False, {'D': ({'A': 0}, {'N': 3, 'I': 2}, {'R': 5})})
        >>>
        """
        equal, diff = super().diff(differ, a, b)

        try:
            diff['D'] = tuple(diff['D'])
        except KeyError:
            pass

        return equal, diff

    def patch(self, patcher, target, diff):
        """
        Return patched tuple.

        :param patcher: nested_diff.Patcher object.
        :param target: tuple to patch.
        :param diff: Nested diff.

        """
        return tuple(super().patch(patcher, list(target), diff))


class SetHandler(TypeHandler):
    """set handler."""

    handled_type = set

    def diff(self, differ, a, b):
        """
        Return diff for two sets.

        :param differ: nested_diff.Differ object.
        :param a: First set to diff.
        :param b: Second set to diff.

        >>> from nested_diff import Differ
        >>>
        >>> a = {1, 2}
        >>> b = {2, 3}
        >>>
        >>> Differ(handlers=[SetHandler()], U=False).diff(a, b)
        (False, {'D': [{'R': 1}, {'A': 3}], 'E': set()})
        >>>
        """
        diff = []
        equal = True

        for i in a.union(b):
            if i in a:
                if i in b:
                    if differ.op_u:
                        diff.append({'U': i})
                elif differ.op_r:
                    # ignore trimR opt here: value required for removal
                    diff.append({'R': i})
                    equal = False
            else:  # added
                if differ.op_a:
                    diff.append({'A': i})
                equal = False

        if diff:
            return equal, {'D': diff, 'E': a.__class__()}

        return equal, {}

    def patch(self, patcher, target, diff):
        """
        Return patched set.

        :param patcher: nested_diff.Patcher object.
        :param target: set to patch.
        :param diff: Nested diff.

        """
        for subdiff in diff['D']:
            try:
                target.add(subdiff['A'])
            except KeyError:
                try:
                    target.remove(subdiff['R'])
                except KeyError:
                    pass

        return target

    def generate_formatted_diff(self, formatter, diff, depth):
        """Generate formatted set diff."""
        for subdiff in diff['D']:
            for tag in ('R', 'A', 'U'):
                try:
                    value = subdiff[tag]
                except KeyError:
                    continue

                yield from formatter.generate_value(value, tag, depth)
                break


class FrozenSetHandler(SetHandler):
    """frozenset handler."""

    handled_type = frozenset

    def patch(self, patcher, target, diff):
        """
        Return patched frozenset.

        :param patcher: nested_diff.Patcher object.
        :param target: frozenset to patch.
        :param diff: Nested diff.

        """
        return frozenset(super().patch(patcher, set(target), diff))


class TextHandler(TypeHandler):
    """text (multiline string) handler."""

    handled_type = str

    def __init__(self, context=3):
        """
        Initialize handler.

        :param context: Amount of context lines.

        """
        super().__init__()
        self.lcs = SequenceMatcher(isjunk=None, autojunk=False)
        self.context = context

    def diff(self, differ, a, b):
        r"""
        Return equality flag and diff for texts (multiline strings).

        Result is a unified-like diff formatted as nested diff structure, with
        'I' tagged subdiffs containing hunks headers.

        :param differ: nested_diff.Differ object.
        :param a: First string to diff.
        :param b: Second string to diff.

        >>> from nested_diff import Differ
        >>>
        >>> a = 'one'
        >>> b = 'one\ntwo'
        >>>
        >>> Differ(handlers=[TextHandler()]).diff(a, b)
        (False,
         {'D': [{'I': [0, 1, 0, 2]}, {'U': 'one'}, {'A': 'two'}], 'E': ''})
        >>>
        """
        lines_a = a.split('\n', -1)
        lines_b = b.split('\n', -1)

        if len(lines_a) == len(lines_b) == 1:
            return super().diff(differ, a, b)

        diff = []
        equal = True

        self.lcs.set_seq1(lines_a)
        self.lcs.set_seq2(lines_b)

        for group in self.lcs.get_grouped_opcodes(self.context):
            diff.append({
                'I': [
                    group[0][1], group[-1][2],
                    group[0][3], group[-1][4],
                ],
            })

            for op, i1, i2, j1, j2 in group:
                if op == 'equal':
                    diff.extend({'U': line} for line in lines_a[i1:i2])
                    continue

                equal = False

                if op != 'insert':
                    diff.extend({'R': line} for line in lines_a[i1:i2])

                if op != 'delete':
                    diff.extend({'A': line} for line in lines_b[j1:j2])

        if diff:
            return equal, {'D': diff, 'E': a.__class__()}

        return equal, {}

    def patch(self, patcher, target, diff):
        """
        Return patched text (multiline string).

        Unlike GNU patch, this algorithm does not implement any heuristics and
        patch target in straightforward way: get position from hunk header and
        apply changes specified in a hunk.

        :param patcher: nested_diff.Patcher object.
        :param target: string to patch.
        :param diff: Nested diff.

        """
        offset = 0
        target = target.split('\n', -1)

        for subdiff in diff['D']:
            if 'I' in subdiff:  # hunk started
                idx = subdiff['I'][0] + offset
            elif 'A' in subdiff:
                target.insert(idx, subdiff['A'])
                offset += 1
                idx += 1
            elif 'R' in subdiff:
                if target.pop(idx) != subdiff['R']:
                    raise ValueError('Removing line does not match')
                offset -= 1
            elif 'U' in subdiff:
                if target[idx] != subdiff['U']:
                    raise ValueError('Unchanged line does not match')
                idx += 1
            else:
                raise ValueError('Unsupported operation')

        return '\n'.join(target)

    def generate_formatted_diff(self, formatter, diff, depth):
        """Generate unified text diff."""
        for subdiff in diff['D']:
            for tag in ('I', 'R', 'A', 'U'):
                try:
                    value = subdiff[tag]
                except KeyError:
                    continue

                if tag == 'I':
                    yield from formatter.generate_string(
                        '@@ -{} +{} @@'.format(
                            self._get_hunk_range(value[0], value[1]),
                            self._get_hunk_range(value[2], value[3]),
                        ),
                        'H',
                        depth,
                    )
                else:
                    yield from formatter.generate_string(value, tag, depth)

    @staticmethod
    def _get_hunk_range(start, stop):
        length = stop - start

        if length > 1:
            return '{},{}'.format(start + 1, length)

        return str(start + 1)
