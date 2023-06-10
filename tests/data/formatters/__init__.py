"""Python specific tests."""

from tests.data import specific, standard


def get_formatter_opt_values_tests():
    return {
        'values_format_default': {
            'diff': {'D': {'KEY': {'A': 'VAL'}, 'key': {'R': 'val'}}},
            'formatter_opts': {'values': None},
        },

        'values_format_disabled': {
            'diff': {'D': {'KEY': {'A': 'VAL'}, 'key': {'R': 'val'}}},
            'formatter_opts': {'values': ''},
        },
        'values_format_unsupported': {
            'diff': {},
            'formatter_opts': {'values': 'unsupported_value'},
            'raises': ValueError,
        },
    }


def get_tests():
    tests = {}
    tests.update(standard.get_tests())
    tests.update(specific.get_tests())
    tests.update(get_formatter_opt_values_tests())

    # structures
    tests.update({
        'brackets': {
            'a': {'[': ']', '{': '}', '(': ')', '<': '>'},
            'b': {'[': '[', '{': '{', '(': '(', '<': '<'},
            'diff': {
                'D': {
                    '(': {'N': '(', 'O': ')'},
                    '<': {'N': '<', 'O': '>'},
                    '[': {'N': '[', 'O': ']'},
                    '{': {'N': '{', 'O': '}'},
                },
            },
        },
        'comments': {
            'diff': {'D': {'k': {'N': 'V', 'O': 'v', 'C': 'C-NO'}}, 'C': 'C-D'},
        },
        'comment_vs_type_hint': {
            'diff': {
                'D': [
                    {'I': [0, 2, 0, 2]},
                    {'R': 'two'},
                    {'A': '2'},
                    {'U': 'lines'},
                ],
                'E': 5,
                'H': 'Comment should win',
            },
            'formatter_opts': {'type_hints': True},  # type hint should be ignored
        },
        'comment_is_empty_string': {
            'diff': {'C': '', 'N': 'new', 'O': 'old'},
        },
        'comment_is_multiline_string': {
            'diff': {'C': 'multi\nline\ncomment', 'N': 'new', 'O': 'old'},
        },
        'comment_with_HTML_tags': {
            'diff': {'U': 'same', 'C': '<h1>comment</h1>'},
        },
        'escaped_symbols': {
            'a': {'\n': '\r\n'},
            'b': {'\n': '\n'},
            'diff': {'D': {'\n': {'N': '\n', 'O': '\r\n'}}},
        },
        'quote_symbols': {
            'a': {'`backticks`': '``', '"double"': '""', "'single'": "''"},
            'b': {'`backticks`': '`', '"double"': '"', "'single'": "'"},
            'diff': {
                'D': {
                    '"double"': {'N': '"', 'O': '""'},
                    '`backticks`': {'N': '`', 'O': '``'},
                    "'single'": {'N': "'", 'O': "''"},
                },
            },
            'formatter_opts': {'sort_keys': True},
        },
        'type_hints_disabled': {
            'a': 'two\nlines',
            'b': '2\nlines',
            'diff': {'D': [{'I': [0, 2, 0, 2]}, {'R': 'two'}, {'A': '2'}, {'U': 'lines'}], 'E': 5},
            'diff_opts': {'text_diff_ctx': 2},
            'formatter_opts': {'type_hints': False},
        },
        'redefined_depth': {
            'a': 0,
            'b': 1,
            'diff': {'N': 1, 'O': 0},
            'format_func_opts': {'depth': 3},
        },
        'unsupported_extension': {
            'diff': {'D': None, 'E': 'garbage'},
            'raises': ValueError,
        },
    })

    for test in tests.values():
        test.setdefault('formatter_opts', {}).setdefault('sort_keys', True)

    return tests
