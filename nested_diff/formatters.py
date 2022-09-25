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

import nested_diff
import nested_diff.handlers

from html import escape as escape_html


class AbstractFormatter(object):
    """Base class for nested diff formatters."""

    def __init__(
        self,
        handlers=None,
        indent='  ',
        line_separator='\n',
        sort_keys=True,
    ):
        """
        Initialize formatter.

        :param handlers: iterable with type handlers.
        :param indent: prefix for each level of diff.
        :param line_separator: text lines delimiter.
        :param sort_keys: sort keys for dict-like structures.

        """
        self.indent = indent
        self.line_separator = line_separator
        self.sort_keys = sort_keys

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
        self.val_line_prefix['H'] = '  '
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

        self.type_prefix = {}
        self.type_suffix = {}

        self.handlers = {}

        if handlers is None:
            handlers = (
                *nested_diff._TYPE_HANDLERS,
                nested_diff.handlers.TextHandler(),
            )

        for handler in handlers:
            self.set_handler(handler)

    def format(self, diff, **kwargs):  # noqa A003
        """Return formatted diff."""
        return ''.join(self.generate_diff(diff, **kwargs))

    def set_handler(self, handler):
        """
        Set handler.

        :param handler: handlers.TypeHandler.

        """
        self.handlers[handler.handled_type] = handler
        self.type_prefix[handler.handled_type] = handler.type_prefix
        self.type_suffix[handler.handled_type] = handler.type_suffix


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

    def generate_comment(self, diff, depth=0):
        """Generate diff comment."""
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

        yield from self.generate_string(comment, tag, depth)

    def generate_diff(self, diff, depth=0, header='', footer=''):
        """Generate formatted diff."""
        yield header

        yield from self.generate_comment(diff, depth=depth)

        try:
            handler = self.handlers[diff['E'].__class__]
        except KeyError:
            try:
                handler = self.handlers[diff['D'].__class__]
            except KeyError:
                handler = nested_diff._DEFAULT_HANDLER

        yield from handler.generate_formatted_diff(self, diff, depth)

        yield footer

    def generate_key(self, key, tag, diff_type, depth):
        """Generate key line."""
        yield self.key_line_prefix[tag]
        yield self.indent * depth
        yield self.key_prefix[tag]
        yield self.type_prefix[diff_type]
        yield self.format_key(key)
        yield self.type_suffix[diff_type]
        yield self.key_suffix[tag]
        yield self.line_separator

    def generate_string(self, value, tag, depth):
        """Generate string line."""
        yield self.val_line_prefix[tag]
        yield self.indent * depth
        yield self.val_prefix[tag]
        yield self.format_string(value)
        yield self.val_suffix[tag]
        yield self.line_separator

    def generate_value(self, value, tag, depth):
        """Generate value line."""
        yield self.val_line_prefix[tag]
        yield self.indent * depth
        yield self.val_prefix[tag]
        yield self.format_value(value)
        yield self.val_suffix[tag]
        yield self.line_separator

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

        for key, val in self.key_line_prefix.items():
            self.key_line_prefix[key] = '<div>' + val
        for key, val in self.val_line_prefix.items():
            self.val_line_prefix[key] = '<div>' + val

        for key in self.key_line_prefix:
            self.key_prefix[key] = '<span class="dif-k' + key + '">'
            self.key_suffix[key] = '</span>'

        for key, val in self.val_prefix.items():
            self.val_prefix[key] = ('<span class="dif-v' + key + '">' +
                                    escape_html(val))
        for key, val in self.val_suffix.items():
            self.val_suffix[key] = escape_html(val) + '</span>'

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
            ' .dif-vA {background-color: #dfd}'
            ' .dif-vC {color: #00b}'
            ' .dif-vE {color: #00b}'
            ' .dif-vH {color: #707}'
            ' .dif-vN {background-color: #dfd}'
            ' .dif-vO {background-color: #fdd}'
            ' .dif-vR {background-color: #fdd}'
            ' .dif-vU {color: #777}'
        )

    def format(self, diff, header='', footer='', **kwargs):  # noqa A003
        """Return completely formatted diff as string."""
        return ''.join(self.generate_diff(
            diff,
            header=header+'<div class="dif-body">',
            footer='</div>'+footer,
            **kwargs,
        ))

    def format_key(self, key):
        """Return key/index representation."""
        return escape_html(super().format_key(key))

    def format_string(self, val):
        """Return string representation."""
        return escape_html(super().format_string(val))

    def format_value(self, val):
        """Return value representation."""
        return escape_html(super().format_value(val))


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
        self.val_line_prefix['H'] = '\033[35m' + self.val_line_prefix['H']
        self.val_line_prefix['N'] = '\033[32m' + self.val_line_prefix['N']
        self.val_line_prefix['O'] = '\033[31m' + self.val_line_prefix['O']
        self.val_line_prefix['R'] = '\033[31m' + self.val_line_prefix['R']
