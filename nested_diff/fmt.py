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

from __future__ import unicode_literals

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
        super(AbstractFormatter, self).__init__(**kwargs)

        self.indent = indent
        self.line_separator = line_separator

        self.open_tokens = {
            dict: '{',
            list: '[',
            set: '{',
            tuple: '(',
        }
        self.close_tokens = {
            dict: '}',
            list: ']',
            set: '}',
            tuple: ')',
        }

        self.diff_tokens = {
            'A': '+ ',
            'D': '  ',
            'N': '+ ',
            'O': '- ',
            'R': '- ',
            'U': '  ',
        }
        self.tags = (  # diff tags to format, sequence is important
            'R',
            'O',
            'N',
            'A',
            'U',
        )

    def format(self, diff):
        """
        Return completely formatted diff

        """
        return ''.join(self.iterate(diff))

    def iterate(self, diff):
        """
        Yield diff token by token

        """
        raise NotImplementedError

    def get_key_prefix(self, tag, depth):
        """
        Return key prefix: diff token (if any) and indent

        """
        return self.diff_tokens[tag] + self.indent * depth

    def get_key_suffix(self):
        """
        Return key suffix

        """
        return self.line_separator

    def get_value_prefix(self, tag, depth):
        """
        Return value prefix: diff token (if any) and indent

        """
        return self.diff_tokens[tag] + self.indent * depth

    def get_value_suffix(self):
        """
        Return value suffix

        """
        return self.line_separator

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
    def iterate(self, diff):
        """
        Yield diff token by token

        """
        depth = 0
        is_new_subdiff = False
        key_tag = 'U'
        stack = [((None, _, False) for _ in (diff,))]

        while True:
            try:
                pointer, diff, is_pointed = next(stack[-1])
            except StopIteration:
                stack.pop()
                if stack:
                    depth -= 1
                    continue
                else:
                    break

            if 'D' in diff:
                stack.append(self.get_iter(diff['D']))

                is_new_subdiff = True
                container_type = diff['D'].__class__
                if is_pointed:
                    yield self.get_key_prefix('D', depth - 1)
                    yield self.get_open_token(container_type)
                    yield self.repr_key(pointer)
                    yield self.get_close_token(container_type)
                    yield self.get_key_suffix()

                depth += 1
                continue

            if is_pointed:
                key_tag = None
            elif is_new_subdiff:
                key_tag = 'U'
                is_new_subdiff = False
                # preamble for collections without pointers such as set
                yield self.get_key_prefix(key_tag, depth - 1)
                yield '<'
                yield container_type.__name__
                yield '>'
                yield self.get_key_suffix()

            for tag in self.tags:
                if tag in diff:
                    if key_tag is None:
                        # key/index
                        key_tag = tag if tag == 'A' or tag == 'R' else 'U'
                        yield self.get_key_prefix(key_tag, depth - 1)
                        yield self.get_open_token(container_type)
                        yield self.repr_key(pointer)
                        yield self.get_close_token(container_type)
                        yield self.get_key_suffix()

                    # value
                    yield self.get_value_prefix(tag, depth)
                    yield self.repr_value(diff[tag])
                    yield self.get_value_suffix()


class TermFormatter(TextFormatter):
    """
    Same as TextFormatter but with term colors.

    """
    def __init__(self, *args, **kwargs):
        super(TermFormatter, self).__init__(*args, **kwargs)

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
            'N': '\033[32m+ ',
            'O': '\033[31m- ',
            'R': '\033[31m- ',
            'U': '  ',
        }

    def get_key_prefix(self, tag, depth):
        """
        Return key prefix: diff token (if any) and indent

        """
        return self.diff_key_tokens[tag] + self.indent * depth

    def get_key_suffix(self):
        """
        Return key suffix

        """
        return '\033[0m' + self.line_separator

    def get_value_prefix(self, tag, depth):
        """
        Return value prefix: diff token (if any) and indent

        """
        return self.diff_value_tokens[tag] + self.indent * depth

    def get_value_suffix(self):
        """
        Return value suffix

        """
        return '\033[0m' + self.line_separator
