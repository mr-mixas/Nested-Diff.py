def get_tests():
    return {
        'frozenset_extended': {
            'a': frozenset((1,)),
            'b': frozenset((1, 2)),
            'diff': {'D': [{'U': 1}, {'A': 2}], 'E': frozenset()},
        },
        'frozensets_lcs': {
            'a': frozenset((1, 2)),
            'b': frozenset((2, 3)),
            'diff': {'D': [{'R': 1}, {'U': 2}, {'A': 3}], 'E': frozenset()},
        },
        'mixed_specific_structures': {
            'a': (tuple(), set()),
            'b': (frozenset(), {True}),
            'diff': {'D': ({'N': frozenset(), 'O': ()}, {'D': [{'A': True}], 'E': set()})},
        },
        'set_extended': {
            'a': {1},
            'b': {1, 2},
            'diff': {'D': [{'U': 1}, {'A': 2}], 'E': set()},
        },
        'sets_lcs': {
            'a': {1, 2},
            'b': {2, 3},
            'diff': {'D': [{'R': 1}, {'U': 2}, {'A': 3}], 'E': set()},
        },
        'sets_lcs_noAR': {
            'a': {1, 2},
            'b': {2, 3},
            'diff': {'D': [{'U': 2}], 'E': set()},
            'diff_opts': {'A': False, 'R': False},
            'patched': {1, 2},
        },
        'sets_lcs_noU': {
            'a': {1, 2},
            'b': {2, 3},
            'diff': {'D': [{'R': 1}, {'A': 3}], 'E': set()},
            'diff_opts': {'U': False},
        },
        'sets_lcs_trimR': {
            'a': {1, 2},
            'b': {2, 3},
            'diff': {'D': [{'R': 1}, {'U': 2}, {'A': 3}], 'E': set()},
            'diff_opts': {'trimR': True},
        },
        'sets_empty_diff': {
            'a': set((1,)),
            'b': set((1, 2)),
            'diff': {},
            'diff_opts': {'A': False, 'U': False},
            'patched': set((1,)),
        },
        'str_multiline_with_multiline_mode_off': {
            'a': 'A\nB',
            'b': 'B\nC',
            'diff': {'N': 'B\nC', 'O': 'A\nB'},
            'diff_opts': {'multiline_diff_context': -1},
        },
        'str_single_line_on_multiline_mode': {
            'a': 'bar',
            'b': 'baz',
            'diff': {'N': 'baz', 'O': 'bar'},
            'diff_opts': {'multiline_diff_context': 3},
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
