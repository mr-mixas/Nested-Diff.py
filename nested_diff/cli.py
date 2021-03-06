# -*- coding: utf-8 -*-
#
# Copyright 2019,2020 Michael Samoglyadov
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
import os
import sys

import nested_diff


class App(object):
    """
    Base class for command line tools

    """
    default_ifmt = 'auto'
    default_ofmt = 'auto'

    supported_ifmts = ('auto', 'ini', 'json', 'yaml')
    supported_ofmts = ('auto', 'ini', 'json', 'yaml')

    version = nested_diff.__version__

    def __init__(self, args=None):
        self.override_excepthook()  # ASAP, but overridable by descendants

        self.argparser = self.get_argparser(description=self.__doc__)
        self.args = self.argparser.parse_args(args=args)

    @staticmethod
    def _decode_fmt_opts(opts):
        if opts is None:
            return {}

        import json
        return json.loads(opts)

    def dump(self, file_, data, fmt):
        self.get_dumper(
            fmt,
            **self._decode_fmt_opts(self.args.ofmt_opts)  # noqa C815
        ).dump(file_, data)

    def get_argparser(self, description=None):
        return argparse.ArgumentParser(
            description=description,
            parents=(
                self.get_optional_args_parser(),
                self.get_positional_args_parser(),
            ),
        )

    def get_optional_args_parser(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s {}'.format(self.version),
            help='print version and exit',
        )

        parser.add_argument(
            '--ifmt',
            type=str,
            default=self.default_ifmt,
            choices=sorted(self.supported_ifmts),
            help='input files format; "' + self.default_ifmt +
            '" used by default',
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
            default=self.default_ofmt,
            choices=sorted(self.supported_ofmts),
            help='output files format; "' + self.default_ofmt +
            '" used by default',
        )

        parser.add_argument(
            '--ofmt-opts',
            metavar='JSON',
            type=str,
            help='output files format options',
        )

        return parser

    @staticmethod
    def get_positional_args_parser():
        return argparse.ArgumentParser(add_help=False)

    @staticmethod
    def get_dumper(fmt, **kwargs):
        if fmt == 'json':
            return JsonDumper(**kwargs)
        elif fmt == 'yaml':
            return YamlDumper(**kwargs)
        elif fmt == 'ini':
            return IniDumper(**kwargs)

        raise RuntimeError('Unsupported output format: ' + fmt)

    @staticmethod
    def guess_fmt(fp, default, ignore_fps=(sys.stdin, sys.stdout, sys.stderr)):
        """
        Guess format of a file object based on its extention.

        """
        if fp in ignore_fps:
            return default

        fmt = os.path.splitext(fp.name)[-1].split('.')[-1].lower()

        if fmt == 'yml':
            fmt = 'yaml'

        return fmt if fmt else default

    @staticmethod
    def get_loader(fmt, **kwargs):
        if fmt == 'json':
            return JsonLoader(**kwargs)
        elif fmt == 'yaml':
            return YamlLoader(**kwargs)
        elif fmt == 'ini':
            return IniLoader(**kwargs)

        raise RuntimeError('Unsupported input format: ' + fmt)

    def load(self, file_):
        if self.args.ifmt == 'auto':
            fmt = self.guess_fmt(file_, 'json')
        else:
            fmt = self.args.ifmt

        fmt_opts = self._decode_fmt_opts(self.args.ifmt_opts)
        return self.get_loader(fmt, **fmt_opts).load(file_)

    @staticmethod
    def override_excepthook():
        """
        Change default exit code for unhandled exceptions from 1 to 127.
        Mainly for diff tool (version control systems treat 1 as difference
        in files).

        """
        def overrided(*args, **kwargs):
            sys.__excepthook__(*args, **kwargs)  # do all the same
            raise SystemExit(127)  # but change exit code

        sys.excepthook = overrided

    def run(self):
        raise NotImplementedError


class Dumper(object):
    """
    Base class for data dumpers

    """
    tty_final_new_line = False

    def encode(self, data):
        raise NotImplementedError

    @staticmethod
    def get_opts(opts):
        return opts

    def dump(self, file_, data):
        file_.write(self.encode(data))

        if self.tty_final_new_line and file_.isatty():
            file_.write('\n')

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
    tty_final_new_line = True

    def __init__(self, **kwargs):
        super().__init__()

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
        super().__init__()

        import json
        self.decoder = json.JSONDecoder(**self.get_opts(kwargs))

    def decode(self, data):
        return self.decoder.decode(data)


class IniDumper(Dumper):
    """
    INI dumper

    """
    def __init__(self, **kwargs):
        super().__init__()

        import configparser
        import io
        self.encoder = configparser.ConfigParser(**self.get_opts(kwargs))
        self.stringio = io.StringIO()

    def encode(self, data):
        self.encoder.read_dict(data)
        self.encoder.write(self.stringio)

        return self.stringio.getvalue()


class IniLoader(Loader):
    """
    INI loader

    """
    def __init__(self, **kwargs):
        super().__init__()

        from configparser import ConfigParser
        self.decoder = ConfigParser(**kwargs)

    def decode(self, data):
        self.decoder.read_string(data)

        out = {}
        for section in self.decoder.sections():
            out[section] = {}
            for option in self.decoder.options(section):
                out[section][option] = self.decoder.get(section, option)

            # cleanup (parser accumulates all readed confs)
            self.decoder.remove_section(section)

        return out


class YamlDumper(Dumper):
    """
    YAML dumper

    All kwargs passed directly to `yaml.safe_dump()`
    `default_flow_style` is set to `False` if absent in kwargs

    """
    def __init__(self, **kwargs):
        super().__init__()

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
        super().__init__()

        import yaml
        self.codec = yaml
        self.codec_opts = self.get_opts(kwargs)

    def decode(self, data):
        return self.codec.safe_load(data, **self.codec_opts)
