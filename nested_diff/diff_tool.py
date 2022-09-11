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

"""Nested diff command line tool."""

import argparse
import sys

import nested_diff
import nested_diff.cli
import nested_diff.handlers


class App(nested_diff.cli.App):
    """Diff tool for nested data structures."""

    supported_ofmts = ('auto', 'html', 'json', 'term', 'toml', 'text', 'yaml')

    def diff(self, a, b, **kwargs):
        """
        Return equality flag and diff for passed objects.

        :param a: First object to diff.
        :param b: Second object to diff.

        kwargs will be merged (with higher priority) with cli options passed
        to Differ().

        """
        diff_opts = {
            'A': self.args.A,
            'N': self.args.N,
            'O': self.args.O,  # noqa: E741
            'R': self.args.R,
            'U': self.args.U,
        }
        diff_opts.update(kwargs)

        if diff_opts['R'] == 'trim':
            diff_opts['R'] = True
            diff_opts['trimR'] = True
        else:
            diff_opts['R'] = int(diff_opts['R'])

        differ = nested_diff.Differ(**diff_opts)

        if self.args.text_ctx >= 0:
            differ.set_handler(nested_diff.handlers.TextHandler(
                context=self.args.text_ctx))

        return differ.diff(a, b)

    def get_optional_args_parser(self):
        """Return parser for optional part (dash prefixed) of CLI args."""
        parser = super().get_optional_args_parser()

        parser.add_argument(
            '--show',
            action='store_true',
            help="don't diff arguments, just format and show them; nested "
                 'diffs expected on input',
        )

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

        parser.add_argument(
            '-q', '--quiet',
            action='store_true',
            help="don't show diff, exit code is the only difference indicator",
        )

        parser.add_argument('-A', type=int, choices=(0, 1), default=1,
                            help='show added items; enabled by default')
        parser.add_argument('-N', type=int, choices=(0, 1), default=1,
                            help="show item's new values; enabled by default")
        parser.add_argument('-O', type=int, choices=(0, 1), default=1,
                            help="show item's old values; enabled by default")
        parser.add_argument('-R', choices=('0', '1', 'trim'), default=1,
                            help='Show removed items; enabled (1) by default. '
                            'Value will be replaced by null when "trim" used')
        parser.add_argument('-U', type=int, choices=(0, 1), default=0,
                            help='show unchanged items; disabled by default')

        return parser

    def get_positional_args_parser(self):
        """Return parser for positional part (files etc) of CLI args."""
        parser = super().get_positional_args_parser()

        parser.add_argument(
            'files',
            metavar='file',
            nargs='+',
            type=argparse.FileType(),
        )

        return parser

    def get_dumper(self, fmt, **kwargs):
        """
        Return data dumper object based on desired format.

        :param kwargs: passed to dumper's constructor as is.

        """
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
        """Diff app object entry point."""
        if self.args.show:
            return self.run_format()

        if len(self.args.files) < 2:
            self.argparser.error('Two or more arguments expected for diff')

        return self.run_diff()

    def run_diff(self):
        """Compute and print diff."""
        if len(self.args.files) > 2:
            if self.args.out.isatty():
                header_template = '\033[33m--- {a}\n+++ {b}\033[0m\n'
            else:
                header_template = '--- {a}\n+++ {b}\n'
        else:
            header_template = ''

        a = None
        exit_code = 0

        for file_ in self.args.files:
            b = {'name': file_.name, 'data': self.load(file_)}

            if a is not None:
                equal, diff = self.diff(a['data'], b['data'])

                if not equal:
                    exit_code = 1

                if self.args.quiet:
                    continue

                header = header_template.format(a=a['name'], b=b['name'])
                self.dump(self.args.out, diff, self.args.ofmt, header=header)

            a = b

        return exit_code

    def run_format(self):
        """Format and print diff."""
        if len(self.args.files) > 1:
            if self.args.out.isatty():
                header_template = '\033[33m=== {filename}\033[0m\n'
            else:
                header_template = '=== {filename}\n'
        else:
            header_template = ''

        for file_ in self.args.files:
            self.dump(
                self.args.out,
                self.load(file_),
                self.args.ofmt,
                header=header_template.format(filename=file_.name),
            )

        return 0


class AbstractFmtDumper(nested_diff.cli.Dumper):
    """Base class for diff formatters dumpers."""

    def encode(self, data):
        """
        Return encoded (formatted) diff.

        :param data: diff data to format.

        """
        return self.encoder.format(data)

    @staticmethod
    def get_opts(opts):
        """
        Return dumper options.

        :param opts: initial options.

        `sort_keys` is set to `True` if absent in opts.

        """
        opts.setdefault('sort_keys', True)
        return opts


class HtmlDumper(AbstractFmtDumper):
    """Human friendly HTML dumper for nested diff."""

    def __init__(self, html_opts=(('lang', 'en'), ('title', 'Nested diff')),
                 **kwargs):
        """
        Initialize dumper.

        :param html_opts: may contain `header` (default is brief HTML5
        boilerplate) and `footer` (page closing tags). Also `lang` and `title`
        supported which define according values for default `header`.

        Rest kwargs passed to `fmt.HtmlFormatter`.

        """
        super().__init__()
        from html import escape
        from nested_diff.formatters import HtmlFormatter

        self.html_opts = dict(html_opts)
        self.formatter = HtmlFormatter(**self.get_opts(kwargs))

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
        """
        Return diff formatted as HTML.

        :param data: diff to format.

        """
        return self.formatter.format(
            data,
            header=self.html_opts['header'],
            footer=self.html_opts['footer'],
        )


class TermDumper(AbstractFmtDumper):
    """Same as TextDumper but with ANSI term colors."""

    def __init__(self, **kwargs):
        """
        Initialize dumper.

        :param kwargs: passed to `fmt.TermFormatter`.

        """
        super().__init__()
        from nested_diff.formatters import TermFormatter
        self.encoder = TermFormatter(**self.get_opts(kwargs))


class TextDumper(AbstractFmtDumper):
    """Human friendly text dumper for nested diff."""

    def __init__(self, **kwargs):
        """
        Initialize dumper.

        :param kwargs: passed to `fmt.TextFormatter` as is.

        """
        super().__init__()
        from nested_diff.formatters import TextFormatter
        self.encoder = TextFormatter(**self.get_opts(kwargs))


def cli():
    """Cli tool entry point."""
    return App().run()
