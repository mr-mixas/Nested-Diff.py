# -*- coding: utf-8 -*-
#
# Copyright 2019-2021 Michael Samoglyadov
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
        Construct diff formatter.

        :param indent: prefix for each level of diff.
        :line_separator: text lines delimiter.

        Rest kwargs are passed to nested_diff.Iterator as is.

        """
        self.iterator = nested_diff.Iterator(**kwargs)
        self.indent = indent
        self.line_separator = line_separator

        self.multiline_header_prefix = '@@ -'
        self.multiline_header_suffix = ' @@'

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
        self.val_line_prefix = self.key_line_prefix.copy()
        self.val_line_prefix['E'] = '# '
        self.val_line_prefix['I'] = '  '
        self.val_line_prefix['O'] = '- '
        self.val_line_prefix['N'] = '+ '

        self.tags = (  # diff tags to format, sequence is important
            'D',
            'R',
            'O',
            'N',
            'A',
            'U',
        )

        self.type_prefix = '<'
        self.type_suffix = '>'

        self.__emitters = {}

    def get_emitter(self, diff, depth=0):
        """Return apropriate tokens emitter for diff extention."""
        try:
            return self.__emitters[diff['E'].__class__](diff, depth=depth)
        except KeyError:
            raise NotImplementedError from None

    @staticmethod
    def get_unified_diff_range(start, stop):
        """Return unified diff lines range."""
        length = stop - start

        if length > 1:
            return '{},{}'.format(start + 1, length)

        return str(start + 1)

    def format(self, diff, **kwargs):
        """Return completely formatted diff as string."""
        return ''.join(self.emit_tokens(diff, **kwargs))

    def set_emitter(self, type_, method):
        """Set tokens emitter for diff extention."""
        self.__emitters[type_] = method


class TextFormatter(AbstractFormatter):
    """Produce human friendly text diff with indenting formatting."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_emitter(frozenset, self.emit_set_tokens)
        self.set_emitter(set, self.emit_set_tokens)
        self.set_emitter(str, self.emit_miltiline_tokens)

    def emit_miltiline_tokens(self, diff, depth=0):
        """Yield unified diff for multiline strings."""
        indent = self.indent * depth

        for subdiff in diff['D']:
            for tag in ('I', 'R', 'A', 'U'):
                if tag in subdiff:
                    yield self.val_line_prefix[tag]
                    yield indent

                    value = subdiff[tag]
                    if tag == 'I':
                        yield self.multiline_header_prefix
                        yield self.get_unified_diff_range(value[0], value[1])
                        yield ' +'
                        yield self.get_unified_diff_range(value[2], value[3])
                        yield self.multiline_header_suffix
                    else:
                        yield from self.repr_string(value, tag)

                    yield self.line_separator

    def emit_set_tokens(self, diff, depth=0):
        """Yield tokens for set's and frozenset's diff."""
        indent = self.indent * depth

        for subdiff in diff['D']:
            for tag in ('R', 'A', 'U'):
                if tag in subdiff:
                    yield self.val_line_prefix[tag]
                    yield indent
                    yield from self.repr_value(subdiff[tag], tag)
                    yield self.line_separator
                    break

    def emit_type_header(self, diff, depth=0):
        """Yield header for non-builtin types."""
        yield self.val_line_prefix['E']
        yield self.indent * depth
        yield self.type_prefix
        yield diff['E'].__class__.__name__
        yield self.type_suffix
        yield self.line_separator

    def emit_tokens(self, diff, depth=0, header='', footer=''):
        """Yield formatted diff token by token."""
        yield header

        for diff, key, subdiff, depth in self.iterator.iterate(diff, depth):
            # emit value
            if 'E' in diff:
                yield from self.emit_type_header(diff, depth=depth)
                yield from self.get_emitter(diff, depth=depth)
                continue

            if subdiff is None:
                for tag in self.tags:
                    if tag in diff:
                        yield self.val_line_prefix[tag]
                        yield self.indent * depth
                        yield from self.repr_value(diff[tag], tag)
                        yield self.line_separator
                continue

            # emit key
            for tag in self.tags:
                if tag in subdiff:
                    yield self.key_line_prefix[tag]
                    yield self.indent * depth
                    yield from self.repr_key(key, tag, diff['D'].__class__)
                    yield self.line_separator
                    break

        yield footer

    def repr_key(self, key, tag, diff_type):
        """Return string representation for key/index."""
        yield self.obj_prefix[diff_type]
        yield key.__repr__()
        yield self.obj_suffix[diff_type]

    @staticmethod
    def repr_string(val, tag):
        yield val

    @staticmethod
    def repr_value(val, tag):
        """Return string representation for value."""
        yield val.__repr__()


class HtmlFormatter(TextFormatter):
    """
    Produce human friendly html diff with indenting formatting.

    Text copied from the browser should be exactly the same as TextFormatter
    produce.

    """

    def __init__(self, *args, line_separator='', **kwargs):
        super().__init__(*args, line_separator=line_separator, **kwargs)

        self.line_separator = '</div>' + self.line_separator

        self.multiline_header_prefix = '<span class="dif-kX0-0">@@ -'
        self.multiline_header_suffix = ' @@</span>'

        for key, val in self.key_line_prefix.items():
            self.key_line_prefix[key] = '<div>' + val
        for key, val in self.val_line_prefix.items():
            self.val_line_prefix[key] = '<div>' + val

        self.type_prefix = '<span class="dif-kE">&lt;'
        self.type_suffix = '&gt;</span>'

        self.key_prefix = {}
        self.key_suffix = {}
        for key in self.key_line_prefix:
            self.key_prefix[key] = '<span class="dif-k' + key + '">'
            self.key_suffix[key] = '</span>'

        self.val_prefix = {}
        self.val_suffix = {}
        for key in self.val_line_prefix:
            self.val_prefix[key] = '<span class="dif-v' + key + '">'
            self.val_suffix[key] = '</span>'

    @staticmethod
    def get_css():
        return (
            '.dif-body {font-family: monospace; white-space: pre}'
            ' .dif-kA {background-color: #cfc}'
            ' .dif-kD {color: #000}'
            ' .dif-kE {color: #00b}'
            ' .dif-kN {color: #000}'
            ' .dif-kO {color: #000}'
            ' .dif-kR {background-color: #fcc}'
            ' .dif-kU {color: #777}'
            ' .dif-kX0-0 {color: #707}'
            ' .dif-vA {background-color: #dfd}'
            ' .dif-vN {background-color: #dfd}'
            ' .dif-vO {background-color: #fdd}'
            ' .dif-vR {background-color: #fdd}'
            ' .dif-vU {color: #777}'
        )

    def emit_tokens(self, diff, depth=0, header='', footer=''):
        """Yield formatted diff token by token."""
        yield from super().emit_tokens(
            diff,
            depth=depth,
            header=header + '<div class="dif-body">',
            footer='</div>' + footer,
        )

    def repr_key(self, key, tag, diff_type):
        """Return string representation for key/index."""
        yield self.key_prefix[tag]
        yield self.obj_prefix[diff_type]
        yield html.escape(key.__repr__())
        yield self.obj_suffix[diff_type]
        yield self.key_suffix[tag]

    def repr_string(self, val, tag):
        yield self.val_prefix[tag]
        yield html.escape(val)
        yield self.val_suffix[tag]

    def repr_value(self, val, tag):
        """Return string representation for value."""
        yield self.val_prefix[tag]
        yield html.escape(val.__repr__())
        yield self.val_suffix[tag]


class TermFormatter(TextFormatter):
    """Same as TextFormatter but with term colors."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.line_separator = '\033[0m' + self.line_separator

        self.key_line_prefix['A'] = '\033[1;32m' + self.key_line_prefix['A']
        self.key_line_prefix['R'] = '\033[1;31m' + self.key_line_prefix['R']

        self.val_line_prefix['A'] = '\033[32m' + self.val_line_prefix['A']
        self.val_line_prefix['E'] = '\033[34m' + self.val_line_prefix['E']
        self.val_line_prefix['I'] = '\033[35m' + self.val_line_prefix['I']
        self.val_line_prefix['N'] = '\033[32m' + self.val_line_prefix['N']
        self.val_line_prefix['O'] = '\033[31m' + self.val_line_prefix['O']
        self.val_line_prefix['R'] = '\033[31m' + self.val_line_prefix['R']
