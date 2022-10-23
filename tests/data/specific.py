def get_tests():
    return {
        'frozenset_extended': {
            'a': frozenset((1,)),
            'b': frozenset((1, 2)),
            'diff': {'D': [{'U': 1}, {'A': 2}], 'E': 4},
        },
        'frozensets_lcs': {
            'a': frozenset((1, 2)),
            'b': frozenset((2, 3)),
            'diff': {'D': [{'R': 1}, {'U': 2}, {'A': 3}], 'E': 4},
        },
        'mixed_specific_structures': {
            'a': ((), set()),
            'b': (frozenset(), {True}),
            'diff': {'D': ({'N': frozenset(), 'O': ()}, {'D': [{'A': True}], 'E': 3})},
        },
        'empty_string_vs_text': {
            'a': '',
            'b': 'A\nB',
            'diff': {
                'D': [
                    {'I': [0, 1, 0, 2]},
                    {'R': ''},
                    {'A': 'A'},
                    {'A': 'B'},
                ],
                'E': 5,
            },
            'diff_opts': {'text_diff_ctx': 3},
        },
        'line_added_to_empty_string': {
            'a': '',
            'b': '\n',
            'diff': {
                'D': [
                    {'I': [0, 1, 0, 2]},
                    {'U': ''},
                    {'A': ''},
                ],
                'E': 5,
            },
            'diff_opts': {'text_diff_ctx': 3},
        },
        'text_equal': {
            'a': 'A\nB\nC',
            'b': 'A\nB\nC',
            'diff': {},
            'diff_opts': {'U': False, 'text_diff_ctx': 3},
        },
        'text_lcs': {
            'a': 'A\nB\nC',
            'b': 'A\nC',
            'diff': {
                'D': [
                    {'I': [0, 3, 0, 2]},
                    {'U': 'A'},
                    {'R': 'B'},
                    {'U': 'C'},
                ],
                'E': 5,
            },
            'diff_opts': {'text_diff_ctx': 3},
        },
        'text_line_added': {
            'a': 'B\nC',
            'b': 'A\nB\nC',
            'diff': {
                'D': [
                    {'I': [0, 2, 0, 3]},
                    {'A': 'A'},
                    {'U': 'B'},
                    {'U': 'C'},
                ],
                'E': 5,
            },
            'diff_opts': {'text_diff_ctx': 3},
        },
        'text_line_changed': {
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
                'E': 5,
            },
            'diff_opts': {'text_diff_ctx': 3},
        },
        'text_line_changed_ctx_0': {
            'a': 'A\nB\nC',
            'b': 'A\nb\nC',
            'diff': {
                'D': [
                    {'I': [1, 2, 1, 2]},
                    {'R': 'B'},
                    {'A': 'b'},
                ],
                'E': 5,
            },
            'diff_opts': {'text_diff_ctx': 0},
        },
        'text_line_removed': {
            'a': 'A\nB\nC',
            'b': 'A\nC',
            'diff': {
                'D': [
                    {'I': [0, 3, 0, 2]},
                    {'U': 'A'},
                    {'R': 'B'},
                    {'U': 'C'},
                ],
                'E': 5,
            },
            'diff_opts': {'text_diff_ctx': 3},
        },
        'text_multiple_hunks': {
            'a': 'A\nB\nC',
            'b': 'A\nA\nB',
            'diff': {
                'D': [
                    {'I': [0, 0, 0, 1]},
                    {'A': 'A'},
                    {'I': [2, 3, 3, 3]},
                    {'R': 'C'},
                ],
                'E': 5,
            },
            'diff_opts': {'text_diff_ctx': 0},
        },
        'text_trailing_newlines': {
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
                'E': 5,
            },
            'diff_opts': {'text_diff_ctx': 3},
        },
        'text_vs_empty_string': {
            'a': 'A\nB',
            'b': '',
            'diff': {
                'D': [
                    {'I': [0, 2, 0, 1]},
                    {'R': 'A'},
                    {'R': 'B'},
                    {'A': ''},
                ],
                'E': 5,
            },
            'diff_opts': {'text_diff_ctx': 3},
        },
        'set_extended': {
            'a': {1},
            'b': {1, 2},
            'diff': {'D': [{'U': 1}, {'A': 2}], 'E': 3},
        },
        'sets_lcs': {
            'a': {1, 2},
            'b': {2, 3},
            'diff': {'D': [{'R': 1}, {'U': 2}, {'A': 3}], 'E': 3},
        },
        'sets_lcs_noAR': {
            'a': {1, 2},
            'b': {2, 3},
            'diff': {'D': [{'U': 2}], 'E': 3},
            'diff_opts': {'A': False, 'R': False},
            'patched': {1, 2},
        },
        'sets_lcs_noU': {
            'a': {1, 2},
            'b': {2, 3},
            'diff': {'D': [{'R': 1}, {'A': 3}], 'E': 3},
            'diff_opts': {'U': False},
        },
        'sets_lcs_trimR': {
            'a': {1, 2},
            'b': {2, 3},
            'diff': {'D': [{'R': 1}, {'U': 2}, {'A': 3}], 'E': 3},
            'diff_opts': {'trimR': True},
        },
        'sets_empty_diff': {
            'a': {1},
            'b': {1, 2},
            'diff': {},
            'diff_opts': {'A': False, 'U': False},
            'patched': {1},
        },
        'text_diff_disabled': {
            'a': 'A\nB',
            'b': 'B\nC',
            'diff': {'N': 'B\nC', 'O': 'A\nB'},
            'diff_opts': {'text_diff_ctx': -1},
        },
        'simple_strings_in_text_mode': {
            'a': 'bar',
            'b': 'baz',
            'diff': {'N': 'baz', 'O': 'bar'},
            'diff_opts': {'text_diff_ctx': 3},
        },
        'str_vs_bytes': {
            'a': 'a',
            'b': b'a',
            'diff': {'N': b'a', 'O': 'a'},
        },
        'tuple_extended': {
            'a': (1,),
            'b': (1, 2),
            'diff': {'D': ({'U': 1}, {'A': 2})},
        },
        'tuples_lcs': {
            'a': (1, 2, 4, 5),
            'b': (0, 1, 2, 3),
            'diff': {'D': ({'A': 0}, {'U': 1}, {'U': 2}, {'N': 3, 'O': 4}, {'R': 5})},
        },
        'tuples_lcs_noOU': {
            'a': (1, 2, 4, 5),
            'b': (0, 1, 2, 3),
            'diff': {'D': ({'A': 0}, {'I': 2, 'N': 3}, {'R': 5})},
            'diff_opts': {'O': False, 'U': False},
        },
    }
