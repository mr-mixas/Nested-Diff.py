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
Patch tool for nested diff.

"""
import argparse
import nested_diff.cli


class App(nested_diff.cli.App):
    """
    Patch tool for nested data structures

    """
    def get_argparser(self, description=None):
        parent = super().get_argparser()
        parser = argparse.ArgumentParser(
            conflict_handler='resolve',
            description=description,
            parents=(parent,)
        )

        return parser

    @staticmethod
    def get_argparser_positional_args():
        yield 'target_file', {}
        yield 'patch_file', {'type': argparse.FileType()}

    @staticmethod
    def patch(target, diff):
        """
        Return patched object

        :param target: object to patch.
        :param diff: nested diff.

        """
        return nested_diff.patch(target, diff)

    def run(self):
        patched = self.patch(
            self.load(argparse.FileType()(self.args.target_file)),
            self.load(self.args.patch_file),
        )

        self.dump(argparse.FileType('w')(self.args.target_file), patched)

        return 0


def cli():
    return App().run()
