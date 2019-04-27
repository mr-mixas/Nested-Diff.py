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
Common stuff for cli tools.

"""
import argparse

import nested_diff


class App(object):
    """
    Base class for command line tools

    """
    version = nested_diff.__version__

    def __init__(self, args=None):
        self.argparser = self.get_argparser(description=self.__doc__)
        self.args = self.argparser.parse_args(args=args)

        self.dumper = self.get_dumper(
            self.args.ofmt,
            **self._decode_fmt_opts(self.args.ofmt_opts)
        )
        self.loader = self.get_loader(
            self.args.ifmt,
            **self._decode_fmt_opts(self.args.ifmt_opts)
        )

    @staticmethod
    def _decode_fmt_opts(opts):
        if opts is None:
            return {}

        import json
        return json.loads(opts)

    def dump(self, file_, data):
        self.dumper.dump(file_, data)

    def get_argparser(self, description=None):
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s {}'.format(self.version),
            help='print version and exit'
        )

        parser.add_argument(
            '--ifmt',
            type=str,
            default='json',
            choices=('json', 'yaml'),
            help='input files format; "json" used by default',
        )

        parser.add_argument(
            '--ifmt-opts',
            metavar='JSON',
            type=str,
            help='input files format options',
        )

        parser.add_argument(
            '--ofmt',
            type=str,
            default='json',
            choices=('json', 'yaml'),
            help='output files format; "json" used by default',
        )

        parser.add_argument(
            '--ofmt-opts',
            metavar='JSON',
            type=str,
            help='output files format options',
        )

        return parser

    @staticmethod
    def get_dumper(fmt, **kwargs):
        if fmt == 'json':
            return JsonDumper(**kwargs)
        elif fmt == 'yaml':
            return YamlDumper(**kwargs)

        raise RuntimeError('Unsupported output format: ' + fmt)

    @staticmethod
    def get_loader(fmt, **kwargs):
        if fmt == 'json':
            return JsonLoader(**kwargs)
        elif fmt == 'yaml':
            return YamlLoader(**kwargs)

        raise RuntimeError('Unsupported input format: ' + fmt)

    def load(self, file_):
        return self.loader.load(file_)

    def run(self):
        raise NotImplementedError


class Dumper(object):
    """
    Base class for data dumpers

    """
    def encode(self, data):
        raise NotImplementedError

    @staticmethod
    def get_opts(opts):
        return opts

    def dump(self, file_, data):
        file_.write(self.encode(data))
        file_.flush()


class Loader(object):
    """
    Base class for data loaders

    """
    def decode(self, data):
        raise NotImplementedError

    @staticmethod
    def get_opts(opts):
        return opts

    def load(self, file_):
        return self.decode(file_.read())


class JsonDumper(Dumper):
    """
    JSON dumper

    All kwargs passed directly to `json.JSONEncoder`
    `indent` is set to 3 and `sort_keys` to `True` if absent in kwargs

    """
    def __init__(self, **kwargs):
        import json
        self.encoder = json.JSONEncoder(**self.get_opts(kwargs))

    def encode(self, data):
        return self.encoder.encode(data)

    @staticmethod
    def get_opts(opts):
        opts.setdefault('indent', 3)
        opts.setdefault('sort_keys', True)
        return opts


class JsonLoader(Loader):
    """
    JSON loader

    All kwargs passed directly to `json.JSONDecoder`

    """
    def __init__(self, **kwargs):
        import json
        self.decoder = json.JSONDecoder(**self.get_opts(kwargs))

    def decode(self, data):
        return self.decoder.decode(data)


class YamlDumper(Dumper):
    """
    YAML dumper

    All kwargs passed directly to `yaml.safe_dump()`
    `default_flow_style` is set to `False` if absent in kwargs

    """
    def __init__(self, **kwargs):
        import yaml
        self.codec = yaml
        self.codec_opts = self.get_opts(kwargs)

    def encode(self, data):
        return self.codec.safe_dump(data, **self.codec_opts)

    @staticmethod
    def get_opts(opts):
        opts.setdefault('default_flow_style', False)
        return opts


class YamlLoader(Loader):
    """
    YAML loader

    All kwargs passed directly to `yaml.safe_load()`

    """
    def __init__(self, **kwargs):
        import yaml
        self.codec = yaml
        self.codec_opts = self.get_opts(kwargs)

    def decode(self, data):
        return self.codec.safe_load(data, **self.codec_opts)
