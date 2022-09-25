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

from warnings import warn

import nested_diff.handlers

__all__ = ['Differ', 'Iterator', 'Patcher', 'diff', 'patch']

__version__ = '0.13'
__author__ = 'Michael Samoglyadov'
__license__ = 'Apache License, Version 2.0'
__website__ = 'https://github.com/mr-mixas/Nested-Diff.py'

_DEFAULT_HANDLER = nested_diff.handlers.TypeHandler()

_TYPE_HANDLERS = (
    nested_diff.handlers.DictHandler(),
    nested_diff.handlers.ListHandler(),
    nested_diff.handlers.TupleHandler(),
    nested_diff.handlers.SetHandler(),
    nested_diff.handlers.FrozenSetHandler(),

    nested_diff.handlers.IntHandler(),
    nested_diff.handlers.FloatHandler(),
    nested_diff.handlers.StrHandler(),
    nested_diff.handlers.BytesHandler(),
)


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
                 trimR=False, handlers=None):
        """
        Initialize Differ.

        Optional arguments:
        `A`, `N`, `O`, `R`, `U` are toggles for according diff ops and all
        enabled (`True`) by default.

        `trimR` when True will drop (replace by `None`) removed data from diff;
        default is `False`.

        `handlers` is a list of type handlers.

        """
        self.op_a = A
        self.op_n = N
        self.op_o = O
        self.op_r = R
        self.op_u = U
        self.op_trim_r = trimR

        self.__differs = {}

        for handler in _TYPE_HANDLERS if handlers is None else handlers:
            self.set_handler(handler)

    def diff(self, a, b):
        """
        Return equality flag and diff for two arbitrary objects.

        This method calls registered handler according diffed objects type.
        Default handler called for objects with different types or when no
        handler registered for such type.

        :param a: First object to diff.
        :param b: Second object to diff.

        """
        if a is b:
            return True, {'U': a} if self.op_u else {}

        if a.__class__ is b.__class__:
            try:
                return self.__differs[a.__class__](self, a, b)
            except KeyError:
                pass

        return self.default_handler.diff(self, a, b)

    def set_handler(self, handler):
        """
        Set handler.

        :param handler: handlers.TypeHandler.

        """
        self.__differs[handler.handled_type] = handler.diff


class Patcher(object):
    """Patch objects using nested diff."""

    default_handler = _DEFAULT_HANDLER

    def __init__(self, handlers=None):
        """
        Initialize Patcher.

        :param handlers: List of type handlers.

        """
        self.__patchers = {}

        for handler in _TYPE_HANDLERS if handlers is None else handlers:
            self.set_handler(handler)

        if handlers is None:
            self.set_handler(nested_diff.handlers.TextHandler())

    def patch(self, target, ndiff):
        """
        Return patched object.

        This method calls apropriate handler for target value according to
        value type.

        :param target: Object to patch.
        :param ndiff: Nested diff.

        """
        if 'D' in ndiff:
            try:
                type_ = ndiff['E'].__class__
            except KeyError:
                type_ = ndiff['D'].__class__

            try:
                return self.__patchers[type_](self, target, ndiff)
            except KeyError:
                raise NotImplementedError('unsupported diff type') from None

        return self.default_handler.patch(self, target, ndiff)

    def set_handler(self, handler):
        """
        Set handler.

        :param handler: handlers.TypeHandler.

        """
        self.__patchers[handler.handled_type] = handler.patch


class Iterator(object):
    """Nested diff iterator."""

    default_handler = _DEFAULT_HANDLER

    def __init__(self, handlers=None, sort_keys=False):
        """
        Initialize iterator.

        If `sort_keys` is `True`, then the output for mappings will be
        sorted by key. Disabled by default.

        `handlers` is a list of type handlers.

        """
        self.sort_keys = sort_keys
        self.__iterators = {}

        for handler in _TYPE_HANDLERS if handlers is None else handlers:
            self.set_handler(handler)

    def _get_iterator(self, ndiff):
        """
        Return apropriate iterator for passed nested diff.

        :param ndiff: nested diff.

        """
        if 'E' in ndiff:
            return self.default_handler.iterate_diff(self, ndiff)

        try:
            return self.__iterators[ndiff['D'].__class__](self, ndiff)
        except KeyError:
            return self.default_handler.iterate_diff(self, ndiff)

    def iterate(self, ndiff, depth=0):
        """
        Yield tuples with diff, key, subdiff and depth for each nested diff.

        :param ndiff: nested diff.
        :param depth: depth initial value (for use in subiterators).

        """
        stack = [self._get_iterator(ndiff)]

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
            stack.append(self._get_iterator(subdiff))

    def set_handler(self, handler):
        """
        Set handler.

        :param handler: handlers.TypeHandler.

        """
        self.__iterators[handler.handled_type] = handler.iterate_diff


def diff(a, b, text_diff_ctx=-1, **kwargs):
    """
    Return recursive diff for two passed objects.

    :param a: First object to diff.
    :param b: Second object to diff.

    :param text_diff_ctx: defines amount of context lines for text (multiline
    strings) diffs, disabled entirely when value is negative. This opt is
    deprecated and should be avoided.

    Rest kwargs passed to Differ's constructor as is.

    """
    differ = Differ(**kwargs)

    if text_diff_ctx >= 0 and kwargs.get('N', True) and kwargs.get('O', True):
        warn('`text_diff_ctx` opt is deprecated and will be removed soon',
             DeprecationWarning, stacklevel=2)

        differ.set_handler(nested_diff.handlers.TextHandler(
            context=text_diff_ctx))

    return differ.diff(a, b)[1]


def patch(target, ndiff, **kwargs):
    """
    Return patched object.

    :param target: Object to patch.
    :param ndiff: Nested diff.

    Rest kwargs passed to Patcher's constructor as is.

    """
    return Patcher(**kwargs).patch(target, ndiff)
