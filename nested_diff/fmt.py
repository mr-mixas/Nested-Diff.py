# -*- coding: utf-8 -*-
#
# Copyright 2019-2022 Michael Samoglyadov
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

"""Formatters for Nested Diff."""

import html

import nested_diff


class AbstractFormatter(object):
    """Base class for nested diff formatters."""

    def __init__(self, indent='  ', line_separator='\n', **kwargs):
        """
        Initialize formatter.

        :param indent: prefix for each level of diff.
        :line_separator: text lines delimiter.

        Rest kwargs passed to nested_diff.Iterator as is.

        """
        self.iterator = nested_diff.Iterator(**kwargs)
        self.indent = indent
        self.line_separator = line_separator

        self.unified_header_prefix = '@@ -'
        self.unified_header_suffix = ' @@'

        self.obj_prefix = {
            dict: '{',
            list: '[',
            tuple: '(',
        }
        self.obj_suffix = {
            dict: '}',
            list: ']',
            tuple: ')',
        }

        self.key_line_prefix = {
            'A': '+ ',
            'D': '  ',
            'N': '  ',
            'O': '  ',
            'R': '- ',
            'U': '  ',
        }

        self.key_prefix = {key: '' for key in self.key_line_prefix}
        self.key_suffix = self.key_prefix.copy()

        self.val_line_prefix = self.key_line_prefix.copy()
        self.val_line_prefix['C'] = '# '
        self.val_line_prefix['E'] = '# '
        self.val_line_prefix['I'] = '  '
        self.val_line_prefix['O'] = '- '
        self.val_line_prefix['N'] = '+ '

        self.val_prefix = {key: '' for key in self.val_line_prefix}
        self.val_suffix = self.val_prefix.copy()

        self.val_prefix['E'] = '<'
        self.val_suffix['E'] = '>'

        self.tags = (  # diff tags to format, sequence is important
            'D',
            'R',
            'O',
            'N',
            'A',
            'U',
        )

        self.__yielders = {}

    def get_yielder(self, diff, depth=0):
        """Return apropriate yielder for diff extention."""
        try:
            return self.__yielders[diff['E'].__class__](diff, depth=depth)
        except KeyError:
            raise NotImplementedError from None

    @staticmethod
    def get_unified_diff_range(start, stop):
        """Return unified diff lines range."""
        length = stop - start

        if length > 1:
            return '{},{}'.format(start + 1, length)

        return str(start + 1)

    def format(self, diff, **kwargs):  # noqa A003
        """Return completely formatted diff as string."""
        return ''.join(self.yield_diff(diff, **kwargs))

    def set_yielder(self, type_, method):
        """Set yielder for diff extention."""
        self.__yielders[type_] = method


class TextFormatter(AbstractFormatter):
    """Produce human friendly text diff with indenting formatting."""

    def __init__(self, *args, type_hints=True, **kwargs):
        """
        Initialize formatter.

        :param type_hints: print values types when True.

        Rest args and kwargs passed to base class as is.

        """
        super().__init__(*args, **kwargs)

        self.type_hints = type_hints

        self.set_yielder(frozenset, self.yield_set_diff)
        self.set_yielder(set, self.yield_set_diff)
        self.set_yielder(str, self.yield_text_diff)

    def yield_text_diff(self, diff, depth=0):
        """Yield unified text diff."""
        indent = self.indent * depth

        for subdiff in diff['D']:
            for tag in ('I', 'R', 'A', 'U'):
                if tag in subdiff:
                    yield self.val_line_prefix[tag]
                    yield indent

                    value = subdiff[tag]
                    if tag == 'I':
                        yield self.unified_header_prefix
                        yield self.get_unified_diff_range(value[0], value[1])
                        yield ' +'
                        yield self.get_unified_diff_range(value[2], value[3])
                        yield self.unified_header_suffix
                    else:
                        yield self.val_prefix[tag]
                        yield self.format_string(value)
                        yield self.val_suffix[tag]

                    yield self.line_separator

    def yield_set_diff(self, diff, depth=0):
        """Yield set and frozenset diff."""
        indent = self.indent * depth

        for subdiff in diff['D']:
            for tag in ('R', 'A', 'U'):
                if tag in subdiff:
                    yield self.val_line_prefix[tag]
                    yield indent
                    yield self.val_prefix[tag]
                    yield self.format_value(subdiff[tag])
                    yield self.val_suffix[tag]
                    yield self.line_separator
                    break

    def yield_comment(self, diff, depth=0):
        """Yield diff comment."""
        try:
            comment = diff['C']
            tag = 'C'
        except KeyError:
            if not self.type_hints:
                return

            try:
                comment = diff['E'].__class__.__name__
                tag = 'E'
            except KeyError:
                return

        yield self.val_line_prefix[tag]
        yield self.indent * depth
        yield self.val_prefix[tag]
        yield self.format_string(comment)
        yield self.val_suffix[tag]
        yield self.line_separator

    def yield_diff(self, diff, depth=0, header='', footer=''):
        """Yield formatted diff."""
        yield header

        for diff, key, subdiff, depth in self.iterator.iterate(diff, depth):  # noqa B020
            yield from self.yield_comment(diff, depth=depth)

            # value
            if 'E' in diff:
                yield from self.get_yielder(diff, depth=depth)
                continue

            if subdiff is None:
                for tag in self.tags:
                    if tag in diff:
                        yield self.val_line_prefix[tag]
                        yield self.indent * depth
                        yield self.val_prefix[tag]
                        yield self.format_value(diff[tag])
                        yield self.val_suffix[tag]
                        yield self.line_separator
                continue

            # key
            for tag in self.tags:
                if tag in subdiff:
                    yield self.key_line_prefix[tag]
                    yield self.indent * depth
                    yield self.key_prefix[tag]
                    yield self.obj_prefix[diff['D'].__class__]
                    yield self.format_key(key)
                    yield self.obj_suffix[diff['D'].__class__]
                    yield self.key_suffix[tag]
                    yield self.line_separator
                    break

        yield footer

    @staticmethod
    def format_key(key):
        """Return key/index representation."""
        return key.__repr__()

    @staticmethod
    def format_string(val):
        """Return string representation."""
        return val

    @staticmethod
    def format_value(val):
        """Return value representation."""
        return val.__repr__()


class HtmlFormatter(TextFormatter):
    """
    Produce human friendly HTML diff with indenting formatting.

    Text copied from the browser should be exactly the same as TextFormatter
    produce.

    """

    def __init__(self, *args, line_separator='', **kwargs):
        """
        Initialize formatter.

        Args and kwargs passed to base class as is.

        """
        super().__init__(*args, line_separator=line_separator, **kwargs)

        self.line_separator = '</div>' + self.line_separator

        self.unified_header_prefix = '<span class="dif-kX0-0">@@ -'
        self.unified_header_suffix = ' @@</span>'

        for key, val in self.key_line_prefix.items():
            self.key_line_prefix[key] = '<div>' + val
        for key, val in self.val_line_prefix.items():
            self.val_line_prefix[key] = '<div>' + val

        for key in self.key_line_prefix:
            self.key_prefix[key] = '<span class="dif-k' + key + '">'
            self.key_suffix[key] = '</span>'

        for key, val in self.val_prefix.items():
            self.val_prefix[key] = ('<span class="dif-v' + key + '">' +
                                    html.escape(val))
        for key, val in self.val_suffix.items():
            self.val_suffix[key] = html.escape(val) + '</span>'

    @staticmethod
    def get_css():
        """Return CSS for generated HTML page."""
        return (
            '.dif-body {font-family: monospace; white-space: pre}'
            ' .dif-kA {background-color: #cfc}'
            ' .dif-kD {color: #000}'
            ' .dif-kN {color: #000}'
            ' .dif-kO {color: #000}'
            ' .dif-kR {background-color: #fcc}'
            ' .dif-kU {color: #777}'
            ' .dif-kX0-0 {color: #707}'
            ' .dif-vA {background-color: #dfd}'
            ' .dif-vC {color: #00b}'
            ' .dif-vE {color: #00b}'
            ' .dif-vN {background-color: #dfd}'
            ' .dif-vO {background-color: #fdd}'
            ' .dif-vR {background-color: #fdd}'
            ' .dif-vU {color: #777}'
        )

    def yield_diff(self, diff, depth=0, header='', footer=''):
        """Yield formatted diff parts."""
        yield from super().yield_diff(
            diff,
            depth=depth,
            header=header + '<div class="dif-body">',
            footer='</div>' + footer,
        )

    def format_key(self, key):
        """Return key/index representation."""
        return html.escape(super().format_key(key))

    def format_string(self, val):
        """Return string representation."""
        return html.escape(super().format_string(val))

    def format_value(self, val):
        """Return value representation."""
        return html.escape(super().format_value(val))


class TermFormatter(TextFormatter):
    """Same as TextFormatter but with term colors."""

    def __init__(self, *args, **kwargs):
        """
        Initialize formatter.

        Args and kwargs passed to base class as is.

        """
        super().__init__(*args, **kwargs)

        self.line_separator = '\033[0m' + self.line_separator

        self.key_line_prefix['A'] = '\033[1;32m' + self.key_line_prefix['A']
        self.key_line_prefix['R'] = '\033[1;31m' + self.key_line_prefix['R']

        self.val_line_prefix['A'] = '\033[32m' + self.val_line_prefix['A']
        self.val_line_prefix['C'] = '\033[34m' + self.val_line_prefix['C']
        self.val_line_prefix['E'] = '\033[34m' + self.val_line_prefix['E']
        self.val_line_prefix['I'] = '\033[35m' + self.val_line_prefix['I']
        self.val_line_prefix['N'] = '\033[32m' + self.val_line_prefix['N']
        self.val_line_prefix['O'] = '\033[31m' + self.val_line_prefix['O']
        self.val_line_prefix['R'] = '\033[31m' + self.val_line_prefix['R']
