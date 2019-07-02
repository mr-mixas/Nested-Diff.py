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

        self.diff_key_tokens = {
            'A': '+ ',
            'D': '  ',
            'N': '+ ',
            'O': '- ',
            'R': '- ',
            'U': '  ',
        }
        self.diff_value_tokens = self.diff_key_tokens.copy()

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
        emit_container_preamble = False
        key_tag = 'U'
        stack = [((None, _, False) for _ in (diff,))]
        path_types = [None]  # even with stack

        while True:
            try:
                pointer, diff, is_pointed = next(stack[-1])
            except StopIteration:
                stack.pop()

                if stack:
                    depth -= 1
                    path_types.pop()
                    container_type = path_types[-1]
                    continue
                else:
                    break

            if 'D' in diff:
                if is_pointed:
                    yield self.diff_key_tokens['D']
                    yield self.indent * (depth - 1)
                    yield self.get_open_token(container_type)
                    yield self.repr_key(pointer)
                    yield self.get_close_token(container_type)
                    yield self.line_separator

                stack.append(self.get_iter(diff['D']))
                container_type = diff['D'].__class__
                path_types.append(container_type)
                emit_container_preamble = True
                depth += 1
                continue

            if is_pointed:
                key_tag = None
            elif emit_container_preamble:  # for keyless collections like set
                key_tag = 'U'
                emit_container_preamble = False
                yield self.diff_key_tokens[key_tag]
                yield self.indent * (depth - 1)
                yield '<'
                yield container_type.__name__
                yield '>'
                yield self.line_separator

            for tag in self.tags:
                if tag in diff:
                    if key_tag is None:
                        # key/index
                        key_tag = tag if tag == 'A' or tag == 'R' else 'U'
                        yield self.diff_key_tokens[key_tag]
                        yield self.indent * (depth - 1)
                        yield self.get_open_token(container_type)
                        yield self.repr_key(pointer)
                        yield self.get_close_token(container_type)
                        yield self.line_separator

                    # value
                    yield self.diff_value_tokens[tag]
                    yield self.indent * depth
                    yield self.repr_value(diff[tag])
                    yield self.line_separator


class TermFormatter(TextFormatter):
    """
    Same as TextFormatter but with term colors.

    """
    def __init__(self, *args, **kwargs):
        super(TermFormatter, self).__init__(*args, **kwargs)

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
            'N': '\033[32m+ ',
            'O': '\033[31m- ',
            'R': '\033[31m- ',
            'U': '  ',
        }
