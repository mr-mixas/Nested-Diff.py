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

        parser.add_argument(
            '--values',
            choices=('repr', 'none', 'json', 'yaml'),
            default='repr',
            help='values format; "none" means no values printed, "repr" is a '
                 'python representation of the object, rest are themselves; '
                 'default is "%(default)s"',
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

        if fmt in FormatterDumper.supported_fmts:
            return FormatterDumper(fmt=fmt, values=self.args.values, **kwargs)

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


class FormatterDumper(nested_diff.cli.Dumper):
    """Nested diff builtin formatters dumper."""

    supported_fmts = ('term', 'text', 'html')

    def __init__(
        self,
        fmt,
        header=None,
        footer=None,
        lang='en',
        title='Nested diff',
        values='repr',
        **kwargs  # noqa C816
    ):
        """Initialize dumper.

        Args:
            fmt: formatter to use.
            header: page header.
            footer: page footer.
            lang: lang HTML option.
            title: HTML page title.
            values: format for values.
            kwargs: Passed to base formatter as is.

        """
        import nested_diff.formatters

        if fmt == 'term':
            base_class = nested_diff.formatters.TermFormatter
        elif fmt == 'html':
            base_class = nested_diff.formatters.HtmlFormatter
        else:
            base_class = nested_diff.formatters.TextFormatter

        fmt_class = self.get_formatter_class(base_class, values=values)
        self.encoder = fmt_class(**self.get_opts(kwargs))

        if header is None:
            if hasattr(self.encoder, 'get_page_header'):
                header = self.encoder.get_page_header(lang=lang, title=title)
            else:
                header = ''

        if footer is None:
            if hasattr(self.encoder, 'get_page_footer'):
                footer = self.encoder.get_page_footer()
            else:
                footer = ''

        super().__init__(header=header, footer=footer)
        self.get_diff_header = self.encoder.get_diff_header

    def encode(self, data):
        """Encode (format) diff.

        Args:
            data: Nested diff to format.

        Returns:
            Encoded diff string.

        """
        return self.encoder.format(data)

    def get_formatter_class(self, base_class, values='repr'):
        """Return formatter class."""

        class __Formatter(base_class):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                if values == 'repr':
                    return

                if values == 'none':
                    self.generate_value = self.generate_empty_value
                    return

                if values == 'json':
                    self.__val_encoder = nested_diff.cli.JsonDumper(indent=2)
                elif values == 'yaml':
                    self.__val_encoder = nested_diff.cli.YamlDumper(
                        explicit_start=False)

                self.generate_value = self.generate_multiline_value

            def generate_empty_value(*args):  # noqa U101
                yield ''

            def generate_multiline_value(self, value, tag, depth):
                for line in self.__val_encoder.encode(value).splitlines():
                    yield from super().generate_string(line, tag, depth)

        return __Formatter

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


def cli():
    """Cli tool entry point."""
    return App().run()
