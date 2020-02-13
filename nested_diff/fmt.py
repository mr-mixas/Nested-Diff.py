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
    def __init__(self, indent='  ', line_separator='\n', **kwargs):
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
            'N': '  ',
            'O': '  ',
            'R': '- ',
            'U': '  ',
        }
        self.diff_value_tokens = self.diff_key_tokens.copy()
        self.diff_value_tokens['H'] = '# '
        self.diff_value_tokens['I'] = '  '
        self.diff_value_tokens['O'] = '- '
        self.diff_value_tokens['N'] = '+ '

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

        return str(start + 1)

    def format(self, diff, **kwargs):
        """
        Return completely formatted diff

        """
        return ''.join(self.emit_tokens(diff, **kwargs))

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


class TextFormatter(AbstractFormatter):
    """
    Produce human friendly text diff with indenting formatting.

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
        indent = self.indent * depth

        for subdiff in diff['D']:
            for tag in ('I', 'R', 'A', 'U'):
                if tag in subdiff:
                    yield self.diff_value_tokens[tag]
                    yield indent
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
        indent = self.indent * depth

        for subdiff in diff['D']:
            for tag in ('R', 'A', 'U'):
                if tag in subdiff:
                    yield self.diff_value_tokens[tag]
                    yield indent
                    yield self.repr_value(subdiff[tag])
                    yield self.line_separator
                    break

    def emit_type_header(self, diff, depth=0):
        yield self.diff_value_tokens['H']
        yield self.indent * depth
        yield '<'
        yield diff['E'].__class__.__name__
        yield '>'
        yield self.line_separator

    def emit_tokens(self, diff, depth=0, header='', footer=''):
        """
        Yield formatted diff token by token

        """
        yield header

        stack = [self.get_iterator(diff)]

        while stack:
            try:
                diff, key, subdiff = next(stack[-1])
            except StopIteration:
                stack.pop()
                depth -= 1
                continue

            # emit value
            if 'E' in diff:
                yield from self.emit_type_header(diff, depth=depth)
                yield from self.get_emitter(diff, depth=depth)
                continue

            if subdiff is None:
                for tag in self.tags:
                    if tag in diff:
                        yield self.diff_value_tokens[tag]
                        yield self.indent * depth
                        yield self.repr_value(diff[tag])
                        yield self.line_separator
                continue

            # emit key
            diff_type = diff['D'].__class__
            for tag in self.tags:
                if tag in subdiff:
                    yield self.diff_key_tokens[tag]
                    yield self.indent * depth
                    yield self.open_tokens[diff_type]
                    yield self.repr_key(key)
                    yield self.close_tokens[diff_type]
                    yield self.line_separator
                    break

            depth += 1
            stack.append(self.get_iterator(subdiff))

        yield footer

    def get_emitter(self, diff, depth=0):
        """
        Return apropriate tokens emitter for diff extention.

        """
        try:
            return self.__emitters[diff['E'].__class__](diff, depth=depth)
        except KeyError:
            raise NotImplementedError from None


class TermFormatter(TextFormatter):
    """
    Same as TextFormatter but with term colors.

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.line_separator = '\033[0m' + self.line_separator

        self.diff_key_tokens['A'] = '\033[1;32m' + self.diff_key_tokens['A']
        self.diff_key_tokens['R'] = '\033[1;31m' + self.diff_key_tokens['R']

        self.diff_value_tokens['A'] = '\033[32m' + self.diff_value_tokens['A']
        self.diff_value_tokens['H'] = '\033[34m' + self.diff_value_tokens['H']
        self.diff_value_tokens['I'] = '\033[35m' + self.diff_value_tokens['I']
        self.diff_value_tokens['N'] = '\033[32m' + self.diff_value_tokens['N']
        self.diff_value_tokens['O'] = '\033[31m' + self.diff_value_tokens['O']
        self.diff_value_tokens['R'] = '\033[31m' + self.diff_value_tokens['R']
