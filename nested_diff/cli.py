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

"""Common stuff for cli tools."""

import argparse
import os
import sys

import nested_diff


class App(object):
    """Base class for command line tools."""

    default_ifmt = 'auto'
    default_ofmt = 'auto'

    supported_ifmts = ('auto', 'ini', 'json', 'toml', 'yaml')
    supported_ofmts = ('auto', 'ini', 'json', 'toml', 'yaml')

    version = nested_diff.__version__

    def __init__(self, args=None):
        """
        Initialize app.

        :param args: command line arguments; `sys.argv` used by default.

        """
        self.override_excepthook()  # ASAP, but overridable by descendants

        self.argparser = self.get_argparser(description=self.__doc__)
        self.args = self.argparser.parse_args(args=args)

    @staticmethod
    def _decode_fmt_opts(opts):
        if opts is None:
            return {}

        import json
        return json.loads(opts)

    def dump(self, file_, data, fmt, header='', footer=''):
        """
        Dump data using apropriate format.

        :param file_: File object to dump.
        :param data: Data to dump.
        :param fmt: Format used for dump, one of `self.supported_ofmts`.
        :param header: Optional leading string.
        :param footer: Optional trailing string.

        """
        if header:
            file_.write(header)

        self.get_dumper(
            fmt,
            **self._decode_fmt_opts(self.args.ofmt_opts)  # noqa C815
        ).dump(file_, data)

        if footer:
            file_.write(footer)

    def get_argparser(self, description=None):
        """Return complete CLI argument parser."""
        return argparse.ArgumentParser(
            description=description,
            parents=(
                self.get_optional_args_parser(),
                self.get_positional_args_parser(),
            ),
        )

    def get_optional_args_parser(self):
        """Return parser for optional part (dash prefixed) of CLI args."""
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
            help='input files format; "%(default)s" is used by default',
        )

        parser.add_argument(
            '--ifmt-opts',
            metavar='JSON',
            type=str,
            help='input files format options (JSON string)',
        )

        parser.add_argument(
            '--ofmt',
            type=str,
            default=self.default_ofmt,
            choices=sorted(self.supported_ofmts),
            help='output files format; "%(default)s" is used by default',
        )

        parser.add_argument(
            '--ofmt-opts',
            metavar='JSON',
            type=str,
            help='output files format options (JSON string)',
        )

        return parser

    @staticmethod
    def get_positional_args_parser():
        """Return parser for positional part (files etc) of CLI args."""
        return argparse.ArgumentParser(add_help=False)

    @staticmethod
    def get_dumper(fmt, **kwargs):
        """
        Return data dumper object based on desired format.

        :param kwargs: passed to dumper's constructor as is.

        """
        if fmt == 'json':
            return JsonDumper(**kwargs)
        elif fmt == 'yaml':
            return YamlDumper(**kwargs)
        elif fmt == 'ini':
            return IniDumper(**kwargs)
        elif fmt == 'toml':
            return TomlDumper(**kwargs)

        raise RuntimeError('Unsupported output format: ' + fmt)

    @staticmethod
    def guess_fmt(fp, default, ignore_fps=(sys.stdin, sys.stdout, sys.stderr)):
        """Guess format of a file object based on its extention."""
        if fp in ignore_fps:
            return default

        fmt = os.path.splitext(fp.name)[-1].split('.')[-1].lower()

        if fmt == 'yml':
            fmt = 'yaml'

        return fmt if fmt else default

    @staticmethod
    def get_loader(fmt, **kwargs):
        """
        Return data loader object based on desired format.

        :param kwargs: passed to loader's constructor as is.

        """
        if fmt == 'json':
            return JsonLoader(**kwargs)
        elif fmt == 'yaml':
            return YamlLoader(**kwargs)
        elif fmt == 'ini':
            return IniLoader(**kwargs)
        elif fmt == 'toml':
            return TomlLoader(**kwargs)

        raise RuntimeError('Unsupported input format: ' + fmt)

    def load(self, file_):
        """
        Load data from file using apropriate loader.

        :param file_: File object to load from.

        """
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
        """
        App object entry point.

        Must be implemented in derivatives.

        """
        raise NotImplementedError


class Dumper(object):
    """Base class for data dumpers."""

    tty_final_new_line = False

    def encode(self, data):
        """
        Return encoded data.

        :param data: data to encode.

        Must be implemented in derivatives.

        """
        raise NotImplementedError

    @staticmethod
    def get_opts(opts):
        """
        Return dumper options.

        :param opts: initial options.

        """
        return opts

    def dump(self, file_, data):
        """
        Encode and write data to file.

        :param file_: File object.
        :param data: Data to write.

        """
        file_.write(self.encode(data))

        if self.tty_final_new_line and file_.isatty():
            file_.write('\n')

        file_.flush()


class Loader(object):
    """Base class for data loaders."""

    def decode(self, data):
        """
        Return decoded data.

        :param data: data to decode.

        Must be implemented in derivatives.

        """
        raise NotImplementedError

    @staticmethod
    def get_opts(opts):
        """
        Return loader options.

        :param opts: initial options.

        """
        return opts

    def load(self, file_):
        """
        Return decoded data loaded from file.

        :param file_: File object.

        """
        return self.decode(file_.read())


class JsonDumper(Dumper):
    """JSON dumper."""

    tty_final_new_line = True

    def __init__(self, **kwargs):
        """
        Initialize dumper.

        :param kwargs: options for `json.JSONEncoder`.

        """
        super().__init__()

        import json
        self.encoder = json.JSONEncoder(**self.get_opts(kwargs))

    def encode(self, data):
        """
        Return JSON encoded data.

        :param data: data to encode.

        """
        return self.encoder.encode(data)

    @staticmethod
    def get_opts(opts):
        """
        Return dumper options.

        :param opts: initial options.

        `indent` is set to 3 and `sort_keys` to `True` if absent in opts.

        """
        opts.setdefault('indent', 3)
        opts.setdefault('sort_keys', True)
        return opts


class JsonLoader(Loader):
    """JSON loader."""

    def __init__(self, **kwargs):
        """
        Initialize loader.

        :param kwargs: options for `json.JSONDecoder`.

        """
        super().__init__()

        import json
        self.decoder = json.JSONDecoder(**self.get_opts(kwargs))

    def decode(self, data):
        """
        Return data decoded from JSON.

        :param data: data to decode.

        """
        return self.decoder.decode(data)


class IniDumper(Dumper):
    """INI dumper."""

    def __init__(self, **kwargs):
        """
        Initialize dumper.

        :param kwargs: options for `configparser.ConfigParser`.

        """
        super().__init__()

        import configparser
        import io
        self.encoder = configparser.ConfigParser(**self.get_opts(kwargs))
        self.stringio = io.StringIO()

    def encode(self, data):
        """
        Return INI encoded data.

        :param data: data to encode.

        """
        self.encoder.read_dict(data)
        self.encoder.write(self.stringio)

        return self.stringio.getvalue()


class IniLoader(Loader):
    """INI loader."""

    def __init__(self, **kwargs):
        """
        Initialize loader.

        :param kwargs: options for `configparser.ConfigParser`.

        """
        super().__init__()

        import configparser
        self.decoder = configparser.ConfigParser(**kwargs)

    def decode(self, data):
        """
        Return data decoded from INI.

        :param data: data to decode.

        """
        self.decoder.read_string(data)

        out = {}
        for section in self.decoder.sections():
            out[section] = {}
            for option in self.decoder.options(section):
                out[section][option] = self.decoder.get(section, option)

            # cleanup (parser accumulates all readed confs)
            self.decoder.remove_section(section)

        return out


class TomlDumper(Dumper):
    """TOML dumper."""

    def __init__(self, **kwargs):
        """Initialize dumper."""
        super().__init__()

        import toml
        self.codec = toml

    def encode(self, data):
        """
        Return TOML encoded data.

        :param data: data to encode.

        """
        return self.codec.dumps(data)


class TomlLoader(Loader):
    """TOML loader."""

    def __init__(self, **kwargs):
        """Initialize loader."""
        super().__init__()

        import toml
        self.codec = toml

    def decode(self, data):
        """
        Return data decoded from TOML.

        :param data: data to decode.

        """
        return self.codec.loads(data)


class YamlDumper(Dumper):
    """YAML dumper."""

    def __init__(self, **kwargs):
        """
        Initialize dumper.

        :param kwargs: options for `yaml.dump`.

        """
        super().__init__()

        import yaml
        try:
            from yaml import CSafeDumper as YamlDumper
        except ImportError:
            from yaml import SafeDumper as YamlDumper

        self.yaml = yaml
        self.yaml_dumper = YamlDumper
        self.opts = self.get_opts(kwargs)

    def encode(self, data):
        """
        Return YAML encoded data.

        :param data: data to encode.

        """
        return self.yaml.dump(data, Dumper=self.yaml_dumper, **self.opts)

    @staticmethod
    def get_opts(opts):
        """
        Return dumper options.

        :param opts: initial options.

        `default_flow_style` is set to `False` if absent in opts.

        """
        opts.setdefault('default_flow_style', False)
        opts.setdefault('explicit_start', True)

        return opts


class YamlLoader(Loader):
    """YAML loader."""

    def __init__(self, **kwargs):
        """
        Initialize loader.

        :param kwargs: options for `yaml.safe_load`.

        """
        super().__init__()

        import yaml
        try:
            from yaml import CSafeLoader as YamlLoader
        except ImportError:
            from yaml import SafeLoader as YamlLoader

        self.yaml = yaml
        self.yaml_loader = YamlLoader
        self.opts = self.get_opts(kwargs)

    def decode(self, data):
        """
        Return data decoded from YAML.

        :param data: data to decode.

        """
        return self.yaml.load(data, Loader=self.yaml_loader, **self.opts)
