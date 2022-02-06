"""Python specific tests."""
from tests.data import standard, specific


def get_tests():
    tests = {}
    tests.update(standard.get_tests())
    tests.update(specific.get_tests())

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
                'E': '',
                'H': 'Comment should win',
            },
            'diff_opts': {'multiline_diff_context': 2},
            'formatter_opts': {'type_hints': True},  # type hint should be ignored
        },
        'comment_is_empty_string': {
            # empty comments should be preserved
            'diff': {'C': '', 'N': 'new', 'O': 'old'},
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
            'diff': {'D': [{'I': [0, 2, 0, 2]}, {'R': 'two'}, {'A': '2'}, {'U': 'lines'}], 'E': ''},
            'diff_opts': {'text_diff_ctx': 2},
            'formatter_opts': {'type_hints': False},
        },
        'wrapping_text': {
            'a': 0,
            'b': 1,
            'diff': {'N': 1, 'O': 0},
            'format_func_opts': {
                'header': 'Header\n',
                'footer': 'Footer\n',
            },
        },
        'redefined_depth': {
            'a': 0,
            'b': 1,
            'diff': {'N': 1, 'O': 0},
            'format_func_opts': {'depth': 3},
        },
        'absent_yielder': {
            'diff': {'D': [], 'E': None},
            'formatter_raises': NotImplementedError,
        },
    })

    for test in tests.values():
        test.setdefault('formatter_opts', {}).setdefault('sort_keys', True)

    return tests
