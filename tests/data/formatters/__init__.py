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
        'wrappings_defined': {
            'a': 0,
            'b': 1,
            'diff': {'N': 1, 'O': 0},
            'formatter_opts': {
                'header': 'Header\n',
                'footer': 'Footer\n',
            },
        },
        'wrappings_undefined': {
            'a': 0,
            'b': 1,
            'diff': {'N': 1, 'O': 0},
            'formatter_opts': {
                'header': None,
                'footer': None,
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

    for test in tests.values():
        test.setdefault('formatter_opts', {}).setdefault('sort_keys', True)

    return tests
