# -*- coding: utf-8 -*-
#
# Copyright 2018-2022 Michael Samoglyadov
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

"""Recursive diff and patch for nested structures."""

from pickle import dumps
from warnings import warn

import nested_diff.handlers

__all__ = ['Differ', 'Iterator', 'Patcher', 'diff', 'patch']

__version__ = '0.10'
__author__ = 'Michael Samoglyadov'
__license__ = 'Apache License, Version 2.0'
__website__ = 'https://github.com/mr-mixas/Nested-Diff.py'

_DEFAULT_HANDLER = nested_diff.handlers.TypeHandler()

# Temporary handlers index
# TODO: turn it to a tuple and use as default handlers after deprecation cycle
_TYPE_HANDLERS = {
    dict: nested_diff.handlers.DictHandler(),
    list: nested_diff.handlers.ListHandler(),
    tuple: nested_diff.handlers.TupleHandler(),
    set: nested_diff.handlers.SetHandler(),
    frozenset: nested_diff.handlers.FrozenSetHandler(),
}


class Differ(object):
    """
    Compute recursive diff for two passed objects.

    Dicts, lists, tuples, sets and frozensets traversed recursively, other
    types compared by values. Any type diff may be customized by user-defined
    type handlers.

    Diff is a dict and may contain status keys:

    `A` stands for 'added', it's value - added item.
    `D` means 'different' and contains subdiff.
    `N` is a new value for changed item.
    `O` is a changed item's old value.
    `R` key used for removed item.
    `U` represent unchanged item.

    and auxiliary keys:

    `C` comment; optional, value - arbitrary string.
    `E` diffed entity (optional), value - empty instance of entity's class.
    `I` index for sequence item, used only when prior item was omitted.

    Diff metadata alternates with actual data; simple types specified as is,
    dicts, lists and tuples contain subdiffs for their items with native for
    such types addressing: indexes for lists and tuples, keys for dictionaries.
    Any status key, except `D` may be omitted during diff computation. `E` key
    is used with `D` when entity unable to contain diff by itself (set,
    frozenset for example); `D` contain a list of subdiffs in this case.

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

    """

    default_handler = _DEFAULT_HANDLER

    def __init__(self, A=True, N=True, O=True, R=True, U=True,  # noqa: E501 E741 N803
                 trimR=False, text_diff_ctx=-1, handlers=()):
        """
        Initialize Differ.

        Optional arguments:
        `A`, `N`, `O`, `R`, `U` are toggles for according diff ops and all
        enabled (`True`) by default.

        `trimR` when True will drop (replace by `None`) removed data from diff;
        default is `False`.

        `text_diff_ctx` defines amount of context lines for text (multiline
        strings) diffs, disabled entirely when value is negative. This opt is
        deprecated and will be removed in the next release.

        `handlers` is a list of type handlers.

        """
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

        self.__handlers = {}

        for handler in handlers:
            self.set_handler(handler)

        if text_diff_ctx >= 0 and self.op_n and self.op_o:
            warn('`text_diff_ctx` opt is deprecated and will be removed in'
                 ' the next release', DeprecationWarning, stacklevel=2)

            self.__handlers[str] = nested_diff.handlers.TextHandler(
                context=text_diff_ctx)
            self.__differs[str] = self.diff_text

    def diff(self, a, b):
        """
        Return diff for two arbitrary objects.

        This method is a dispatcher and calls registered diff method for each
        diffed values pair according to their type. `diff__default` called for
        unequal and not registered types. Args passed to called method as is.

        :param a: First object to diff.
        :param b: Second object to diff.

        """
        if a.__class__ is b.__class__:
            # it's faster to compare pickled dumps and dig differences
            # afterwards than recursively diff each pair of objects
            if a is b or dumps(a, -1) == dumps(b, -1):
                return {'U': a} if self.op_u else {}

            # TODO: get rid of `get_differ` and get funcs directly
            return self.get_differ(a.__class__)(a, b)

        return self.diff__default(a, b)

    def diff__default(self, a, b):
        """Return default diff."""
        warn('`diff__default` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return self.default_handler.diff(self, a, b)

    def diff_dict(self, a, b):
        """
        Return diff for two dicts.

        :param a: First dict to diff.
        :param b: Second dict to diff.

        """
        warn('`diff_dict` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return _TYPE_HANDLERS[dict].diff(self, a, b)

    def diff_list(self, a, b):
        """
        Return diff for two lists.

        :param a: First list to diff.
        :param b: Second list to diff.

        """
        warn('`diff_list` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return _TYPE_HANDLERS[list].diff(self, a, b)

    def diff_text(self, a, b):
        r"""
        Return diff for texts (multiline strings).

        Result is a unified-like diff formatted as nested diff structure, with
        'I' tagged subdiffs containing hunks headers.

        :param a: First string to diff.
        :param b: Second string to diff.

        """
        warn('`diff_text` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return self.__handlers[str].diff(self, a, b)

    def diff_set(self, a, b):
        """
        Return diff for two [frozen]sets.

        :param a: First set to diff.
        :param b: Second set to diff.

        """
        warn('`diff_set` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return _TYPE_HANDLERS[set].diff(self, a, b)

    def diff_tuple(self, a, b):
        """
        Return diff for two tuples.

        :param a: First tuple to diff.
        :param b: Second tuple to diff.

        """
        warn('`diff_tuple` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return _TYPE_HANDLERS[tuple].diff(self, a, b)

    def get_differ(self, type_):
        """
        Return diff method for specified type.

        :param type_: diffed object type.

        """
        warn('`get_differ` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

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
        warn('`set_differ` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        self.__differs[type_] = method

    def set_handler(self, handler):
        """
        Set handler.

        :param handler: handlers.TypeHandler.

        """
        self.__differs[handler.handled_type] = lambda a, b: handler.diff(
            self, a, b)


class Patcher(object):
    """Patch objects using nested diff."""

    default_handler = _DEFAULT_HANDLER

    def __init__(self, handlers=()):
        """
        Initialize Patcher.

        :param handlers: List of type handlers.

        """
        self.__patchers = {
            dict: self.patch_dict,
            frozenset: self.patch_frozenset,
            list: self.patch_list,
            set: self.patch_set,
            str: self.patch_text,
            tuple: self.patch_tuple,
        }

        self.__handlers = {}

        for handler in handlers:
            self.set_handler(handler)

        self.set_handler(nested_diff.handlers.TextHandler())

    def get_patcher(self, type_):
        """
        Return patch method for specified type.

        :param type_: patched object type.

        """
        warn('`get_patcher` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

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
        # TODO: get rid of `get_patcher` and get funcs directly
        if 'D' in ndiff:
            return self.get_patcher(
                ndiff['E' if 'E' in ndiff else 'D'].__class__,
            )(target, ndiff)

        return self.default_handler.patch(self, target, ndiff)

    def patch_dict(self, target, ndiff):
        """
        Return patched dict.

        :param target: dict to patch.
        :param ndiff: Nested diff.

        """
        warn('`patch_dict` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return _TYPE_HANDLERS[dict].patch(self, target, ndiff)

    def patch_list(self, target, ndiff):
        """
        Return patched list.

        :param target: list to patch.
        :param ndiff: Nested diff.

        """
        warn('`patch_list` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return _TYPE_HANDLERS[list].patch(self, target, ndiff)

    def patch_text(self, target, ndiff):
        """
        Return patched text (multiline string).

        Unlike GNU patch, this algorithm does not implement any heuristics and
        patch target in straightforward way: get position from hunk header and
        apply changes specified in hunk.

        :param target: string to patch.
        :param ndiff: Nested diff.

        """
        warn('`patch_text` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return self.__handlers[str].patch(self, target, ndiff)

    def patch_set(self, target, ndiff):
        """
        Return patched set.

        :param target: set to patch.
        :param ndiff: Nested diff.

        """
        warn('`patch_set` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return _TYPE_HANDLERS[set].patch(self, target, ndiff)

    def patch_tuple(self, target, ndiff):
        """
        Return patched tuple.

        :param target: tuple to patch.
        :param ndiff: Nested diff.

        """
        warn('`patch_tuple` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return _TYPE_HANDLERS[tuple].patch(self, target, ndiff)

    def patch_frozenset(self, target, ndiff):
        """
        Return patched frozenset.

        :param target: frozenset to patch.
        :param ndiff: Nested diff.

        """
        warn('`patch_frozenset` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        return _TYPE_HANDLERS[frozenset].patch(self, target, ndiff)

    def set_patcher(self, type_, method):
        """
        Set patcher for specified data type.

        :param type_: patched object type.
        :param method: patch method.

        """
        warn('`set_patcher` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        self.__patchers[type_] = method

    def set_handler(self, handler):
        """
        Set handler.

        :param handler: handlers.TypeHandler.

        """
        self.__patchers[handler.handled_type] = lambda a, b: handler.patch(
            self, a, b)


class Iterator(object):
    """Nested diff iterator."""

    default_handler = _DEFAULT_HANDLER

    def __init__(self, handlers=(), sort_keys=False):
        """
        Initialize iterator.

        If `sort_keys` is `True`, then the output for mappings will be
        sorted by key. Disabled by default.

        `handlers` is a list of type handlers.

        """
        self.sort_keys = sort_keys

        self.__iterators = {
            dict: self.iterate_mapping_diff,
            list: self.iterate_sequence_diff,
            tuple: self.iterate_sequence_diff,
        }

        self.__handlers = {}

        for handler in handlers:
            self.set_handler(handler)

    def iterate__default(self, ndiff):
        """
        Yield final diff (do not iterate deeper).

        :param ndiff: nested diff.

        """
        warn('`iterate__default` is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        yield from self.default_handler.iterate_diff(self, ndiff)

    def iterate_mapping_diff(self, ndiff):
        """
        Iterate over dict-like nested diffs.

        :param ndiff: nested diff.

        """
        warn('`iterate_mapping_diff` is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        yield from _TYPE_HANDLERS[dict].iterate_diff(self, ndiff)

    def iterate_sequence_diff(self, ndiff):
        """
        Iterate over lists, tuples and alike nedsted diffs.

        :param ndiff: nested diff.

        """
        warn('`iterate_sequence_diff` is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        yield from _TYPE_HANDLERS[list].iterate_diff(self, ndiff)

    def get_iterator(self, ndiff):
        """
        Return apropriate iterator for passed nested diff.

        :param ndiff: nested diff.

        """
        warn('`get_iterator` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

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
        warn('`set_iterator` method is deprecated and will be removed in'
             ' the next release', DeprecationWarning, stacklevel=2)

        self.__iterators[type_] = method

    def iterate(self, ndiff, depth=0):
        """
        Yield tuples with diff, key, subdiff and depth for each nested diff.

        :param ndiff: nested diff.
        :param depth: depth initial value (for use in subiterators).

        """
        # TODO: get rid of `get_iterator` and get funcs directly
        stack = [self.get_iterator(ndiff)]

        while stack:
            try:
                ndiff, key, subdiff = next(stack[-1])
            except StopIteration:
                stack.pop()
                depth -= 1
                continue

            yield ndiff, key, subdiff, depth

            if subdiff is None:
                continue

            depth += 1
            stack.append(self.get_iterator(subdiff))

    def set_handler(self, handler):
        """
        Set handler.

        :param handler: handlers.TypeHandler.

        """
        self.__iterators[handler.handled_type] = \
            lambda ndiff: handler.iterate_diff(self, ndiff)


def diff(a, b, **kwargs):
    """
    Return recursive diff for two passed objects.

    :param a: First object to diff.
    :param b: Second object to diff.

    kwargs passed to Differ's constructor as is.

    """
    return Differ(**kwargs).diff(a, b)


def patch(target, ndiff, **kwargs):
    """
    Return patched object.

    :param target: Object to patch.
    :param ndiff: Nested diff.

    kwargs passed to Patcher's constructor as is.

    """
    return Patcher(**kwargs).patch(target, ndiff)
