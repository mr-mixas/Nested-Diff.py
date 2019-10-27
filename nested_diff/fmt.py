# -*- coding: utf-8 -*-
#
# Copyright 2019 Michael Samoglyadov
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
Formatters for Nested Diff.

"""
import nested_diff


class AbstractFormatter(nested_diff.Iterator):
    """
    Base class for nested diff formatters

    """
    def __init__(
        self,
        indent='  ',
        line_separator='\n',
        **kwargs
    ):
        super().__init__(**kwargs)

        self.indent = indent
        self.line_separator = line_separator

        self.open_tokens = {
            dict: '{',
            list: '[',
            tuple: '(',
        }
        self.close_tokens = {
            dict: '}',
            list: ']',
            tuple: ')',
        }

        self.diff_key_tokens = {
            'A': '+ ',
            'D': '  ',
            'I': '  ',
            'N': '+ ',
            'O': '- ',
            'R': '- ',
            'U': '  ',
        }
        self.diff_value_tokens = self.diff_key_tokens.copy()

        self.tags = (  # diff tags to format, sequence is important
            'D',
            'R',
            'O',
            'N',
            'A',
            'U',
        )

    @staticmethod
    def get_unified_diff_range(start, stop):
        """
        Return unified diff lines range.

        """
        length = stop - start

        if length > 1:
            return '{},{}'.format(start + 1, length)

        if length == 1:
            return str(start + 1)

        return '{},{}'.format(start, length)

    def format(self, diff, **kwargs):
        """
        Return completely formatted diff

        """
        return ''.join(self.emit_tokens(diff, **kwargs))

    def get_open_token(self, type_):
        """
        Return open token for specified container's type

        """
        return self.open_tokens[type_]

    def get_close_token(self, type_):
        """
        Return close token for specified container's type

        """
        return self.close_tokens[type_]

    @staticmethod
    def repr_key(key):
        """
        Return string representation for key/index

        """
        return key.__repr__()

    @staticmethod
    def repr_value(val):
        """
        Return string representation for value

        """
        return val.__repr__()

    def set_open_token(self, type_, token):
        """
        Set open token for specified container's type

        """
        self.open_tokens[type_] = token

    def set_close_token(self, type_, token):
        """
        Set close token for specified container's type

        """
        self.close_tokens[type_] = token


class TextFormatter(AbstractFormatter):
    """
    Produce human friendly text diff representation with indenting formatting.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__emitters = {
            frozenset: self.emit_set_tokens,
            set: self.emit_set_tokens,
            str: self.emit_miltiline_tokens,
        }

    def emit_miltiline_tokens(self, diff, depth=0):
        """
        Yield unified diff for multiline strings.

        """
        for subdiff in diff['D']:
            for tag in ('I', 'R', 'A', 'U'):
                if tag in subdiff:
                    yield self.diff_value_tokens[tag]
                    yield self.indent * depth
                    if tag == 'I':
                        yield '@@'
                        yield ' -' + self.get_unified_diff_range(
                            subdiff[tag][0], subdiff[tag][1])
                        yield ' +' + self.get_unified_diff_range(
                            subdiff[tag][2], subdiff[tag][3]) + ' '
                        yield '@@'
                    else:
                        yield subdiff[tag]
                    yield self.line_separator

    def emit_set_tokens(self, diff, depth=0):
        """
        Yield tokens for set's and frozenset's diff

        """
        yield self.diff_key_tokens['D']
        yield self.indent * depth
        yield '<'
        yield diff['E'].__class__.__name__
        yield '>'
        yield self.line_separator

        depth += 1

        for subdiff in diff['D']:
            for tag in ('R', 'A', 'U'):
                if tag in subdiff:
                    yield self.diff_value_tokens[tag]
                    yield self.indent * depth
                    yield self.repr_value(subdiff[tag])
                    yield self.line_separator
                    break

    def get_emitter(self, diff, depth=0):
        """
        Return apropriate tokens emitter for diff extention.

        """
        try:
            return self.__emitters[diff['E'].__class__](diff, depth=depth)
        except KeyError:
            raise NotImplementedError from None

    def emit_tokens(self, diff, depth=0, header='', footer=''):
        """
        Yield formatted diff token by token

        """
        if header:
            yield header
            yield self.line_separator

        key_tag = 'D'

        for depth, container_type, pointer, diff in self.iterate(
                diff, depth=depth):

            for tag in self.tags:
                if tag in diff:
                    # key/index
                    if key_tag is None:
                        key_tag = 'D' if tag in ('O', 'N') else tag
                        yield self.diff_key_tokens[key_tag]
                        yield self.indent * (depth - 1)
                        yield self.get_open_token(container_type)
                        yield self.repr_key(pointer)
                        yield self.get_close_token(container_type)
                        yield self.line_separator

                    # value
                    if tag == 'D':
                        if 'E' in diff:
                            yield from self.get_emitter(diff, depth=depth)
                        break

                    yield self.diff_value_tokens[tag]
                    yield self.indent * depth
                    yield self.repr_value(diff[tag])
                    yield self.line_separator

            key_tag = None

        if footer:
            yield footer
            yield self.line_separator


class TermFormatter(TextFormatter):
    """
    Same as TextFormatter but with term colors.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.line_separator = '\033[0m' + self.line_separator

        self.diff_key_tokens = {
            'A': '\033[1;32m+ ',
            'D': '  ',
            'N': '\033[1;32m+ ',
            'O': '\033[1;31m- ',
            'R': '\033[1;31m- ',
            'U': '  ',
        }
        self.diff_value_tokens = {
            'A': '\033[32m+ ',
            'D': '  ',
            'I': '\033[35m  ',
            'N': '\033[32m+ ',
            'O': '\033[31m- ',
            'R': '\033[31m- ',
            'U': '  ',
        }
