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
        """Calculate diff for two objects.

        Args:
            a: First object to diff.
            b: Second object to diff.
            kwargs: Merged (with higher priority) with cli options and passed
                to nested_diff.Differ constructor.

        Returns:
            Tuple: equality flag and nested diff.

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

    def generate_diffs(self):
        """Generate diffs."""
        a = None
        headers_enabled = False

        if self.args.show:
            if len(self.args.files) > 1:
                headers_enabled = True
        else:
            if len(self.args.files) < 2:
                self.argparser.error('Two or more arguments expected for diff')
            elif len(self.args.files) > 2:
                headers_enabled = True

        for file_ in self.args.files:
            header = ''

            if self.args.show:
                if headers_enabled:
                    header = self.dumper.get_diff_header(
                        '/dev/null (' + file_.name + ')',
                        '/dev/null (' + file_.name + ')',
                    )
                diff = self.load(file_)
                equal = not diff or 'U' in diff
            else:
                b = {'name': file_.name, 'data': self.load(file_)}

                if a is None:
                    a = b
                    continue

                equal, diff = self.diff(a['data'], b['data'])

                if headers_enabled:
                    header = self.dumper.get_diff_header(a['name'], b['name'])

                a = b

            yield header, equal, diff

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
        """Create dumper object according to passed format.

        Args:
            fmt: Dumper format.
            kwargs: Passed to dumper's constructor as is.

        Returns:
            Dumper object.

        """
        if fmt == 'auto':
            if self.args.out.isatty():
                fmt = 'term'
            else:
                fmt = 'text'

        if fmt == 'term':
            return TermDumper(**kwargs)
        if fmt == 'text':
            return TextDumper(**kwargs)
        if fmt == 'html':
            return HtmlDumper(**kwargs)

        return super().get_dumper(fmt, **kwargs)

    def run(self):
        """Diff app object entry point."""
        exit_code = 0

        self.args.out.write(self.dumper.header)

        for diff_header, equal, diff in self.generate_diffs():
            if not equal:
                exit_code = 1

            if self.args.quiet:
                continue

            self.args.out.write(diff_header)
            self.dumper.dump(self.args.out, diff)

        self.args.out.write(self.dumper.footer)

        return exit_code


class AbstractFmtDumper(nested_diff.cli.Dumper):
    """Base class for diff formatters dumpers."""

    def encode(self, data):
        """Encode (format) diff.

        Args:
            data: Nested diff to format.

        Returns:
            Encoded diff string.

        """
        return self.encoder.format(data)

    @staticmethod
    def get_opts(opts):
        """Extend options by default values.

        sort_keys opt is set to `True` if absent in passed opts.

        Args:
            opts: Initial options (dict).

        Returns:
            Options extended by default values.

        """
        opts.setdefault('sort_keys', True)
        return opts


class HtmlDumper(AbstractFmtDumper):
    """Human friendly HTML dumper for nested diff."""

    def __init__(
        self,
        header=None,
        footer=None,
        lang='en',
        title='Nested diff',
        **kwargs  # noqa C816
    ):
        """Initialize dumper.

        Args:
            header: HTML page header. Brief HTML5 boilerplate used by default.
            footer: HTML page closing tags.
            lang: Value for lang HTML option.
            title: HTML page title.
            kwargs: Passed to `fmt.HtmlFormatter` as is.

        """
        from nested_diff.formatters import HtmlFormatter

        self.encoder = HtmlFormatter(**self.get_opts(kwargs))
        self.get_diff_header = self.encoder.get_diff_header

        if header is None:
            header = self.encoder.get_page_header(lang=lang, title=title)

        if footer is None:
            footer = self.encoder.get_page_footer()

        super().__init__(header=header, footer=footer)


class TermDumper(AbstractFmtDumper):
    """Same as TextDumper but with ANSI term colors."""

    def __init__(self, **kwargs):
        """Initialize dumper.

        Args:
            kwargs: Passed to `fmt.TermFormatter` as is.

        """
        super().__init__()
        from nested_diff.formatters import TermFormatter
        self.encoder = TermFormatter(**self.get_opts(kwargs))
        self.get_diff_header = self.encoder.get_diff_header


class TextDumper(AbstractFmtDumper):
    """Human friendly text dumper for nested diff."""

    def __init__(self, **kwargs):
        """Initialize dumper.

        Args:
            kwargs: Passed to `fmt.TextFormatter` as is.

        """
        super().__init__()
        from nested_diff.formatters import TextFormatter
        self.encoder = TextFormatter(**self.get_opts(kwargs))
        self.get_diff_header = self.encoder.get_diff_header


def cli():
    """Cli tool entry point."""
    return App().run()
