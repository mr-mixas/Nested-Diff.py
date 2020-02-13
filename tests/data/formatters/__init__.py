"""
python specific tests

"""
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
        'absent_emitter': {
            'diff': {'D': [], 'E': None},
            'formatter_raises': NotImplementedError,
        },
    })

    # multiline strings
    tests.update({
        'multiline__equal': {
            'a': 'A\nB\nC',
            'b': 'A\nB\nC',
            'diff': {},
            'diff_opts': {'U': False, 'multiline_diff_context': 3},
        },
        'multiline__empty_vs_multiline': {
            'a': '',
            'b': 'A\nB',
            'diff': {
                'D': [
                    {'I': [0, 1, 0, 2]},
                    {'R': ''},
                    {'A': 'A'},
                    {'A': 'B'},
                ],
                'E': '',
            },
            'diff_opts': {'multiline_diff_context': 3},
        },
        'multiline__vs_empty': {
            'b': '',
            'a': 'A\nB',
            'diff': {
                'D': [
                    {'I': [0, 2, 0, 1]},
                    {'R': 'A'},
                    {'R': 'B'},
                    {'A': ''},
                ],
                'E': '',
            },
            'diff_opts': {'multiline_diff_context': 3},
        },
        'multiline__empty_line_added': {
            'a': '',
            'b': '\n',
            'diff': {
                'D': [
                    {'I': [0, 1, 0, 2]},
                    {'U': ''},
                    {'A': ''},
                ],
                'E': '',
            },
            'diff_opts': {'multiline_diff_context': 3},
        },
        'multiline__line_added': {
            'a': 'B\nC',
            'b': 'A\nB\nC',
            'diff': {
                'D': [
                    {'I': [0, 2, 0, 3]},
                    {'A': 'A'},
                    {'U': 'B'},
                    {'U': 'C'},
                ],
                'E': '',
            },
            'diff_opts': {'multiline_diff_context': 3},
        },
        'multiline__line_changed': {
            'a': 'A\nB\nC',
            'b': 'A\nb\nC',
            'diff': {
                'D': [
                    {'I': [0, 3, 0, 3]},
                    {'U': 'A'},
                    {'R': 'B'},
                    {'A': 'b'},
                    {'U': 'C'},
                ],
                'E': '',
            },
            'diff_opts': {'multiline_diff_context': 3},
        },
        'multiline__line_changed_ctx_0': {
            'a': 'A\nB\nC',
            'b': 'A\nb\nC',
            'diff': {
                'D': [
                    {'I': [1, 2, 1, 2]},
                    {'R': 'B'},
                    {'A': 'b'},
                ],
                'E': '',
            },
            'diff_opts': {'multiline_diff_context': 0},
        },
        'multiline__line_removed': {
            'a': 'A\nB\nC',
            'b': 'A\nC',
            'diff': {
                'D': [
                    {'I': [0, 3, 0, 2]},
                    {'U': 'A'},
                    {'R': 'B'},
                    {'U': 'C'},
                ],
                'E': '',
            },
            'diff_opts': {'multiline_diff_context': 3},
        },
        'multiline__trailing_newlines': {
            'a': 'A\nB\n',
            'b': 'A\nb\n',
            'diff': {
                'D': [
                    {'I': [0, 3, 0, 3]},
                    {'U': 'A'},
                    {'R': 'B'},
                    {'A': 'b'},
                    {'U': ''},
                ],
                'E': '',
            },
            'diff_opts': {'multiline_diff_context': 3},
        },
    })

    for test in tests.values():
        test.setdefault('formatter_opts', {}).setdefault('sort_keys', True)

    return tests
