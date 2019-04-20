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
        return nested_diff.diff(a, b, U=False)

    def get_argparser(self, description=None):
        parent = super(App, self).get_argparser()
        parser = argparse.ArgumentParser(
            conflict_handler='resolve',
            description=description,
            parents=(parent,)
        )

        parser.add_argument('file1', type=argparse.FileType())
        parser.add_argument('file2', type=argparse.FileType())

        parser.add_argument(
            '--out',
            default=sys.stdout,
            metavar='FILE',
            type=argparse.FileType('w'),
            help='output file; STDERR is used if omitted',
        )

        return parser

    def run(self):
        diff = self.diff(
            self.load(self.args.file1),
            self.load(self.args.file2),
        )

        self.dump(self.args.out, diff)


def cli():
    App().run()


if __name__ == '__main__':
    App().run()
