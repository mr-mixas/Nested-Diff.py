"""Backward compatibility module."""

from warnings import warn

from nested_diff.formatters import TextFormatter, HtmlFormatter, TermFormatter  # noqa F401


warn('`nested_diff.fmt` module is deprecated and will be removed soon.'
     ' `nested_diff.formatters.py` should be used instead.',
     DeprecationWarning, stacklevel=2)
