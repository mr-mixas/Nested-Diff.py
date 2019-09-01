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
Nested diff command line tool.

"""
import argparse
import sys

import nested_diff
import nested_diff.cli


class App(nested_diff.cli.App):
    """
    Diff tool for nested data structures

    """
    def diff(self, a, b):
        """
        Return diff for passed objects

        :param a: First object to diff.
        :param b: Second object to diff.

        """
        return nested_diff.diff(
            a, b,
            multiline_diff_context=self.args.text_ctx,
            A=self.args.A,
            N=self.args.N,
            O=self.args.O,
            R=self.args.R,
            U=self.args.U,
        )

    def get_argparser(self, description=None):
        parent = super().get_argparser()
        parser = argparse.ArgumentParser(
            conflict_handler='resolve',
            description=description,
            parents=(parent,)
        )

        parser.add_argument('file1', type=argparse.FileType())
        parser.add_argument('file2', type=argparse.FileType())

        parser.add_argument(
            '--text-ctx',
            default=3,
            metavar='NUM',
            type=int,
            help='amount of context lines for multiline strings diffs; ' +
                 'negative value will disable multiline diffs, default is 3'
        )

        parser.add_argument(
            '--ifmt',
            type=str,
            default='json',
            choices=('ini', 'json', 'yaml'),
            help='input files format; "json" used by default',
        )

        parser.add_argument(
            '--ofmt',
            type=str,
            default='auto',
            choices=('auto', 'json', 'term', 'text', 'yaml'),
            help='output format',
        )

        parser.add_argument(
            '--out',
            default=sys.stdout,
            metavar='FILE',
            type=argparse.FileType('w'),
            help='output file; STDERR is used if omitted',
        )

        parser.add_argument('-A', type=int, choices=(0, 1), default=1,
                            help='show added items; enabled by deefault')
        parser.add_argument('-N', type=int, choices=(0, 1), default=1,
                            help='show item\'s new values; enabled by default')
        parser.add_argument('-O', type=int, choices=(0, 1), default=1,
                            help='show item\'s old values; enabled by default')
        parser.add_argument('-R', type=int, choices=(0, 1), default=1,
                            help='Show removed items; enabled by default')
        parser.add_argument('-U', type=int, choices=(0, 1), default=0,
                            help='show unchanged items; disabled by default')

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

        return super().get_dumper(fmt, **kwargs)

    def get_loader(self, fmt, **kwargs):
        if fmt == 'ini':
            return nested_diff.cli.IniLoader(**kwargs)

        return super().get_loader(fmt, **kwargs)

    def run(self):
        diff = self.diff(
            self.load(self.args.file1),
            self.load(self.args.file2),
        )

        self.dump(self.args.out, diff)


class AbstractFmtDumper(nested_diff.cli.Dumper):
    def __init__(self, **kwargs):
        super().__init__()
        import nested_diff.fmt

    def encode(self, data):
        return self.encoder.format(data)

    @staticmethod
    def get_opts(opts):
        opts.setdefault('sort_keys', True)
        return opts


class TermDumper(AbstractFmtDumper):
    def __init__(self, **kwargs):
        super().__init__()
        self.encoder = nested_diff.fmt.TermFormatter(**self.get_opts(kwargs))


class TextDumper(AbstractFmtDumper):
    def __init__(self, **kwargs):
        super().__init__()
        self.encoder = nested_diff.fmt.TextFormatter(**self.get_opts(kwargs))


def cli():
    App().run()


if __name__ == '__main__':
    App().run()