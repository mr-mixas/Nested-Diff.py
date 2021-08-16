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

"""Nested diff command line tool."""

import argparse
import sys

import nested_diff
import nested_diff.cli


class App(nested_diff.cli.App):
    """Diff tool for nested data structures."""

    supported_ofmts = ('auto', 'html', 'json', 'term', 'toml', 'text', 'yaml')

    def diff(self, a, b, **kwargs):
        """
        Return diff for passed objects.

        :param a: First object to diff.
        :param b: Second object to diff.

        kwargs will be merged (with higher priority) with cli options passed
        to Differ().

        """
        diff_opts = {
            'text_diff_ctx': self.args.text_ctx,
            'A': self.args.A,
            'N': self.args.N,
            'O': self.args.O,  # noqa: E741
            'R': self.args.R,
            'U': self.args.U,
        }
        diff_opts.update(kwargs)

        return nested_diff.diff(a, b, **diff_opts)

    def get_optional_args_parser(self):
        parser = super().get_optional_args_parser()

        parser.add_argument(
            '--text-ctx',
            default=3,
            metavar='NUM',
            type=int,
            help='amount of context lines for text (multiline strings) diffs; '
                 'negative value will disable such diffs, default is '
                 '"%(default)s"',
        )

        parser.add_argument(
            '--out',
            default=sys.stdout,
            metavar='FILE',
            type=argparse.FileType('w'),
            help='output file; STDOUT is used if omitted',
        )

        parser.add_argument('-A', type=int, choices=(0, 1), default=1,
                            help='show added items; enabled by default')
        parser.add_argument('-N', type=int, choices=(0, 1), default=1,
                            help="show item's new values; enabled by default")
        parser.add_argument('-O', type=int, choices=(0, 1), default=1,
                            help="show item's old values; enabled by default")
        parser.add_argument('-R', type=int, choices=(0, 1), default=1,
                            help='Show removed items; enabled by default')
        parser.add_argument('-U', type=int, choices=(0, 1), default=0,
                            help='show unchanged items; disabled by default')

        return parser

    def get_positional_args_parser(self):
        parser = super().get_positional_args_parser()

        parser.add_argument('file1', type=argparse.FileType())
        parser.add_argument('file2', type=argparse.FileType())

        return parser

    def get_dumper(self, fmt, **kwargs):
        if fmt == 'auto':
            if self.args.out.isatty():
                fmt = 'term'
            else:
                fmt = 'text'

        if fmt == 'term':
            return TermDumper(**kwargs)
        elif fmt == 'text':
            return TextDumper(**kwargs)
        elif fmt == 'html':
            return HtmlDumper(**kwargs)

        return super().get_dumper(fmt, **kwargs)

    def run(self):
        diff = self.diff(
            self.load(self.args.file1),
            self.load(self.args.file2),
        )
        exit_code = 0 if not diff or 'U' in diff else 1

        self.dump(self.args.out, diff, self.args.ofmt)

        return exit_code


class AbstractFmtDumper(nested_diff.cli.Dumper):
    """Base class for diff dumpers."""

    def encode(self, data):
        return self.encoder.format(data)

    @staticmethod
    def get_opts(opts):
        opts.setdefault('sort_keys', True)
        return opts


class HtmlDumper(AbstractFmtDumper):
    """Human friendly HTML dumper for nested diff."""

    def __init__(self, **kwargs):
        super().__init__()
        from html import escape
        from nested_diff import fmt
        self.html_opts = {
            'lang': 'en',
            'title': 'Nested diff',
        }
        self.html_opts.update(kwargs.pop('html_opts', {}))

        self.formatter = fmt.HtmlFormatter(**self.get_opts(kwargs))

        if 'header' not in self.html_opts:
            self.html_opts['header'] = (
                '<!DOCTYPE html><html lang="' + self.html_opts['lang'] +
                '"><head><title>' + escape(self.html_opts['title']) +
                '</title><style>' + self.formatter.get_css() +
                '</style></head><body>'
            )
        if 'footer' not in self.html_opts:
            self.html_opts['footer'] = '</body></html>'

    def encode(self, data):
        return self.formatter.format(
            data,
            header=self.html_opts['header'],
            footer=self.html_opts['footer'],
        )


class TermDumper(AbstractFmtDumper):
    """Same as TextDumper but with ANSI term colors."""

    def __init__(self, **kwargs):
        super().__init__()
        from nested_diff import fmt
        self.encoder = fmt.TermFormatter(**self.get_opts(kwargs))


class TextDumper(AbstractFmtDumper):
    """Human friendly text dumper for nested diff."""

    def __init__(self, **kwargs):
        super().__init__()
        from nested_diff import fmt
        self.encoder = fmt.TextFormatter(**self.get_opts(kwargs))


def cli():
    """Cli tool entry point."""
    return App().run()
